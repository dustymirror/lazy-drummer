# Lazy Drummer

**Lazy Drummer** is a little Eurorack Europi program to play beats.

**[中文说明 (Chinese)](#-中文说明)**

---

## English Description

### Overview

Lazy Drummer is a dual-channel drum synthesis script for EuroPi. It generates Kick and HiHat sounds directly from CV outputs without samples. It tends to lose the beat quite a bit at slightly faster speeds, so it’s rather lazy.
### Features

- Dual drum synthesis: Kick (square wave decay), HiHat (pulse noise)
- 6 CV outputs: Kick audio, Hat audio, trigger pulses, continuous square wave
- External triggering: DIN → Kick, AIN → HiHat
- Accent: B1/B2 buttons for velocity enhancement
- Minimal UI: Letters show trigger status with subtle animations
- Knob control: K1 controls Kick decay, K2 controls HiHat decay

### CV Output Map

| CV | Signal | Description |
|----|--------|-------------|
| CV1 | Kick audio | Square wave kick |
| CV2 | Continuous square | 60Hz clock/modulation |
| CV3 | Hat audio | Pulse noise hihat |
| CV4 | Kick trigger | 2ms 5V pulse |
| CV5 | Hat gate | 10V during Hat playback |
| CV6 | Hat trigger | 2ms 5V pulse |

### Controls

| Control | Function |
|---------|----------|
| K1 | Kick decay (10-80ms) |
| K2 | HiHat decay (10-50ms) |
| B1 | Kick accent (velocity ×2) |
| B2 | HiHat accent (10V vs 6V) |
| DIN | Trigger Kick |
| AIN | Trigger HiHat (>1V) |

### Installation

1. Copy `lazy_drummer.py` to EuroPi's `lib` folder
2. Launch from the EuroPi main menu
3. Connect CV outputs to external VCO/VCA or mixer
4. Trigger via DIN/AIN inputs, or test with buttons

---

##  中文说明

### 概述

Lazy Drummer 是一个基于 EuroPi 的双通道鼓合成程序。它利用 CV 输出直接合成 Kick（底鼓）和 HiHat（镲片）声音，无任何采样文件。它在稍快的速度会跟丢掉不少节拍，所以挺懒。

### 功能特性

- **双鼓合成**：Kick 使用方波衰减合成，HiHat 使用脉冲噪声合成
- **6 个 CV 输出**：Kick 音频、Hat 音频、触发脉冲、持续方波等
- **外部触发**：DIN 触发 Kick，AIN 触发 HiHat
- **重音 (Accent)**：B1/B2 按钮提供力度增强
- **旋钮控制**：K1 控制 Kick 衰减，K2 控制 HiHat 衰减

### CV 输出分配

| CV | 信号 | 说明 |
|----|------|------|
| CV1 | Kick 音频 | 方波底鼓 |
| CV2 | 持续方波 | 60Hz 方波，可作时钟 |
| CV3 | Hat 音频 | 脉冲噪声镲片 |
| CV4 | Kick 触发脉冲 | 2ms 5V 脉冲 |
| CV5 | Hat 同步方波 | Hat 播放期间 10V |
| CV6 | Hat 触发脉冲 | 2ms 5V 脉冲 |

### 控制说明

| 控件 | 功能 |
|------|------|
| K1 | Kick 衰减时长 (10-80ms) |
| K2 | HiHat 衰减时长 (10-50ms) |
| B1 | Kick 重音 (力度 ×2) |
| B2 | HiHat 重音 (10V vs 6V) |
| DIN | 触发 Kick |
| AIN | 触发 HiHat (电压 > 1V) |

### 安装与使用

1. 将 `lazy_drummer.py` 复制到 EuroPi 的 `lib` 目录
2. 从主菜单选择 Lazy Drummer 启动
3. 连接 CV 输出到外部 VCO/VCA 或混音器
4. 通过 DIN/AIN 输入触发信号，或使用按钮手动测试

---

## Notes / 备注

- HiHat triggering via AIN may experience occasional missed triggers due to EuroPi's analog input hardware limitation (no interrupt support). For critical applications, route your trigger signal through an external comparator to DIN.
- AIN 触发 HiHat 可能偶尔丢失触发，这是 EuroPi 模拟输入无硬件中断的固有限制。关键应用建议将触发信号通过外部比较器转为 DIN 输入。

---

## Version / 版本

**v1.11**

---

## License / 许可

MIT License
