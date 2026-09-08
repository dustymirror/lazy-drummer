from europi import *
from europi_script import EuroPiScript
import random
import time


class LazyDrummer(EuroPiScript):
    
    def __init__(self):
        super().__init__()
        
        self.KICK_MIN_DECAY_MS = 10
        self.KICK_MAX_DECAY_MS = 80
        self.HAT_MIN_DECAY_MS = 10
        self.HAT_MAX_DECAY_MS = 50
        self.TRIGGER_THRESHOLD = 1.8
        
        self.TRIGGER_PULSE_MS = 2
        
        self.kick_decay_ms = 40
        self.hat_decay_ms = 25
        self.kick_accent = False
        self.hat_accent = False
        
        self.kick_playing = False
        self.hat_playing = False
        self.kick_abort = False
        self.hat_abort = False
        
        self.last_ain_state = False
        
        self.last_kick_time = 0
        self.last_hat_time = 0
        
        # A 动画变量
        self.a_display_char = 'A'
        self.a_animation_end_time = 0
        
        self.last_square_toggle_us = time.ticks_us()
        self.square_state = False
        
        # Trigger queue
        self.kick_pending = 0
        self.hat_pending = 0

        self.kick_pending_accent = False
        self.hat_pending_accent = False

        # Display throttling
        self.last_display_update = 0
        self.DISPLAY_INTERVAL_MS = 50
        
        @din.handler
        def on_din():
            self.kick_pending += 1
            self.kick_pending_accent = b1.value()
        
        cv1.voltage(0)
        cv2.voltage(0)
        cv3.voltage(0)
        cv4.voltage(0)
        cv5.voltage(0)
        cv6.voltage(0)
    
    def send_kick_trigger(self):
        cv4.voltage(5.0)
        time.sleep_ms(self.TRIGGER_PULSE_MS)
        cv4.voltage(0)
    
    def send_hat_trigger(self):
        cv6.voltage(5.0)
        time.sleep_ms(self.TRIGGER_PULSE_MS)
        cv6.voltage(0)
    
    def play_kick(self):
        if self.kick_playing:
            self.kick_abort = True
            time.sleep_ms(1)
        
        self.last_kick_time = time.ticks_ms()
        self.kick_playing = True
        self.kick_abort = False
        
        velocity = 2.0 if self.kick_accent else 1.0
        max_voltage = min(10.0, 5.0 * velocity)
        
        self.send_kick_trigger()
        
        decay_us = self.kick_decay_ms * 1000
        period_us = 2000
        steps = max(1, int(decay_us / period_us))
        
        for step in range(steps):
            if self.kick_abort:
                break
            t = step / steps
            freq = 80 + 420 * (1 - t)
            period_us = int(1000000 / freq)
            half_us = period_us // 2
            amp = (1 - t) ** 1.2
            
            cv1.voltage(max_voltage * amp)
            time.sleep_us(half_us)
            cv1.voltage(0)
            time.sleep_us(half_us)
        
        cv1.voltage(0)
        self.kick_playing = False
    
    def play_hihat(self):
        if self.hat_playing:
            self.hat_abort = True
            time.sleep_ms(1)
        
        self.last_hat_time = time.ticks_ms()
        self.hat_playing = True
        self.hat_abort = False
        
        if self.hat_accent:
            max_voltage = 10.0
        else:
            max_voltage = 6.0
        
        self.send_hat_trigger()
        cv5.voltage(10.0)
        
        decay_us = self.hat_decay_ms * 1000
        period_us = 200
        steps = max(1, int(decay_us / period_us))
        if steps > 250:
            steps = 250
        
        for step in range(steps):
            if self.hat_abort:
                break
            t = step / steps
            amp = (1 - t) ** 0.8
            
            duty = random.uniform(0.15, 0.6)
            high_us = int(period_us * duty)
            low_us = period_us - high_us
            
            cv3.voltage(max_voltage * amp)
            time.sleep_us(high_us)
            cv3.voltage(0)
            time.sleep_us(low_us)
        
        cv3.voltage(0)
        cv5.voltage(0)
        self.hat_playing = False
    
    def check_ain_trigger(self):
        current = ain.read_voltage()
        is_high = current > self.TRIGGER_THRESHOLD

        if is_high and not self.last_ain_state:
            self.hat_pending += 1
            self.hat_pending_accent = b2.value()

        self.last_ain_state = is_high

    def process_pending(self):
        if self.kick_pending > 0:
            self.kick_pending -= 1
            self.kick_accent = self.kick_pending_accent
            self.play_kick()

        if self.hat_pending > 0:
            self.hat_pending -= 1
            self.hat_accent = self.hat_pending_accent
            self.play_hihat()
    
    def update_continuous_square(self):
        current_us = time.ticks_us()
        period_us = 16666
        half_period = period_us // 2
        
        if current_us - self.last_square_toggle_us >= half_period:
            self.square_state = not self.square_state
            cv2.voltage(5.0 if self.square_state else 0.0)
            self.last_square_toggle_us = current_us
    
    def update_controls(self):
        self.kick_decay_ms = self.KICK_MIN_DECAY_MS + k1.percent() * (self.KICK_MAX_DECAY_MS - self.KICK_MIN_DECAY_MS)
        self.hat_decay_ms = self.HAT_MIN_DECAY_MS + k2.percent() * (self.HAT_MAX_DECAY_MS - self.HAT_MIN_DECAY_MS)
    
    def update_display(self):
        current_ms = time.ticks_ms()

        if current_ms - self.last_display_update < self.DISPLAY_INTERVAL_MS:
            return

        self.last_display_update = current_ms

        oled.fill(0)
        
        kick_active = (current_ms - self.last_kick_time) < 300
        hat_active = (current_ms - self.last_hat_time) < 300
        
        # 任一触发时，A 进入动画状态
        any_trigger = kick_active or hat_active
        
        if any_trigger:
            # 检查是否需要更新随机字符（每400ms重新随机，或首次触发）
            if self.a_animation_end_time == 0 or current_ms > self.a_animation_end_time:
                # 随机选择 O 或 -
                self.a_display_char = 'O' if random.choice([True, False]) else '-'
                self.a_animation_end_time = current_ms + 666
        else:
            # 无触发时，恢复为 A
            self.a_display_char = 'A'
            self.a_animation_end_time = 0
        
        # 显示
        oled.text('K' if kick_active else 'k', 16, 8)
        oled.text(self.a_display_char, 64, 20)
        oled.text('H' if hat_active else 'h', 112, 8)
        
        if b1.value():
            oled.text('!', 6, 8)
        if b2.value():
            oled.text('!', 122, 8)
        
        oled.show()
    
    def main(self):
        time.sleep(0.5)
        
        try:
            while True:
                self.check_ain_trigger()
                self.process_pending()
                self.update_controls()
                self.update_continuous_square()
                self.update_display()
                time.sleep_ms(1)
        
        except KeyboardInterrupt:
            cv1.voltage(0)
            cv2.voltage(0)
            cv3.voltage(0)
            cv4.voltage(0)
            cv5.voltage(0)
            cv6.voltage(0)
            oled.fill(0)
            oled.show()


if __name__ == "__main__":
    LazyDrummer().main()
