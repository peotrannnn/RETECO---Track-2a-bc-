# Báo cáo chất lượng dữ liệu — domain `robotics`

*Tạo lúc 2026-11-21T09:07:37 | RETECO Track 2 / Data Quality | pha: integrity, content, conversation, gold, link, retrieval, splits*

## 1. Health score

**Tổng: 78.5 🟡** (xanh ≥85, vàng ≥70).

| Nhóm | Trọng số | Điểm | Trạng thái |
| :--- | ---: | ---: | ---: |
| integrity | 0.2 | 99.1 | 🟢 |
| content | 0.25 | 28.6 | 🔴 |
| conversation | 0.15 | 95.0 | 🟢 |
| gold | 0.25 | 92.8 | 🟢 |
| link | 0.15 | 93.6 | 🟢 |

**Top điểm trừ:**

| Nhóm | Nguyên nhân | Giá trị | Hệ số | Trừ |
| :--- | ---: | ---: | ---: | ---: |
| content | % trùng chính xác | 34.75 | 1.0 | 34.75 |
| content | % doc quá ngắn | 39.15 | 0.5 | 19.57 |
| content | % nghi không phải tiếng Anh | 16.41 | 0.5 | 8.21 |
| gold | % gold có lỗi nội dung nghiêm trọng | 14.49 | 0.5 | 7.25 |
| content | % ký hiệu lạ/URL nặng | 15.47 | 0.4 | 6.19 |
| link | % turn gold không chia sẻ từ nào với query | 4.0 | 1.5 | 6.0 |
| conversation | % hội thoại có tham chiếu lơ lửng ở turn đầu | 5.0 | 1 | 5.0 |
| content | % lặp bất thường | 2.26 | 0.5 | 1.13 |
| content | % gần trùng (ngoài trùng chính xác) | 1.54 | 0.7 | 1.08 |
| integrity | % doc có mojibake | 0.31 | 2 | 0.62 |
| content | % boilerplate | 1.4 | 0.3 | 0.42 |
| link | % OOV trung bình của query | 1.18 | 0.3 | 0.35 |

## 2. Khuyến nghị

- **[medium]** 0.31% doc có dấu hiệu lỗi encoding.
- **[medium]** Rỗng 0.0% / quá ngắn 39.15%.
- **[medium]** Trùng chính xác 34.75%.
- **[medium]** Gần trùng 1.54% (MinHash).
- **[low]** 16.41% doc nghi không phải tiếng Anh.
- **[high]** 67.27% turn sau turn đầu phụ thuộc ngữ cảnh -> cần query rewriter.
- **[medium]** 1 hội thoại có đại từ/liên từ ở turn đầu.
- **[medium]** 14.49% gold doc có lỗi nội dung nghiêm trọng.

## 3. Toàn vẹn cấu trúc

- File: `documents.jsonl` ✅ | `benchmark_dev.json` ✅ | `qrels_dev.txt` ✅
- Documents: **61,961** | schema `content, doc_id` | JSON lỗi 0 (0.0%) | không phải object 0 | thiếu id 0 | id trùng 0 | thiếu text 0 | text sai kiểu 0 | title rỗng 0
- Encoding: mojibake 0.31% | ký tự điều khiển 0.12% | HTML/entity sót 0.07%
- Benchmark: 20 hội thoại | schema=`qa_pair` | vai trò {'user': 75, 'assistant': 75} | role không xen kẽ 0 | hội thoại rỗng 0 | conv_id trùng 0 | qid qrels khớp 75/75
- qrels: 147 dòng | malformed 0 | cặp trùng 0 | mức relevance {1: 147} | qid 75

## 4. Chất lượng nội dung

- Ký tự: min=3 p25=23.0 **median=81.0** mean=291.1 p75=214.0 p90=751.0 p99=2889.0 max=28640 | outlier dài (>787.0c): 9.61%
- Tỷ lệ doc ≤ 650/800/1500/3000 ký tự: 88.88% / 90.53% / 93.65% / 99.1%

**Histogram độ dài:**

| Khoảng (ký tự) | % doc |
| :--- | ---: |
| 0-100 | 55.43% |
| 101-300 | 25.64% |
| 301-650 | 7.8% |
| 651-800 | 1.65% |
| 801-1500 | 3.13% |
| 1501-3000 | 5.44% |
| 3001-6000 | 0.84% |
| >6000 | 0.06% |

**Cờ lỗi:**

| Cờ | Mô tả | Số doc | % |
| :--- | ---: | ---: | ---: |
| empty | tài liệu rỗng | 0 | 0.0% |
| too_short | quá ngắn (<50 ký tự) | 24256 | 39.15% |
| mojibake | lỗi encoding (mojibake) | 189 | 0.31% |
| control_chars | ký tự điều khiển | 74 | 0.12% |
| html_residue | HTML/entity còn sót | 44 | 0.07% |
| boilerplate | boilerplate/menu/footer | 866 | 1.4% |
| url_heavy | URL chiếm >25% nội dung | 6878 | 11.1% |
| symbol_heavy | ký hiệu lạ >30% | 2705 | 4.37% |
| repetitive | lặp từ/dòng bất thường | 1400 | 2.26% |
| non_english | nghi không phải tiếng Anh | 10167 | 16.41% |
| pii_email | chứa email | 209 | 0.34% |
| pii_phone | chứa số điện thoại | 60 | 0.1% |
| possibly_truncated | nghi bị cắt cụt (không dấu câu cuối) | 8069 | 13.02% |
| starts_lower | bắt đầu bằng chữ thường | 7544 | 12.18% |

- Doc có ≥1 lỗi NGHIÊM TRỌNG: **64.4%**
- Trùng chính xác: 21,530 doc dư (34.75%), 4213 nhóm
- Gần trùng: 675 cụm | doc dư gần-trùng ngoài trùng chính xác 182 (1.54%) | cụm lớn nhất 25
- Từ vựng (mẫu 10,056 doc): 28,541 từ | hapax 49.78% | Zipf -1.121 | 0(12126), rpm(11955), 1(10841), fc40(8650), noarch(6863), 2(6006), 3(4515), html(4513), 64(4271), x86(4210), devel(3949), ros(3467), 4(3040), fc41(2976), rust(2562)

## 5. Hội thoại

- **20** hội thoại, **75** turn | turn/hội thoại: mean 3.75 (min 3, max 6) | query: mean 18.4 từ, median 18.0, p95 24.0
- Query rỗng 0 | trùng 0 (0.0%) | ≤2 từ 0.0%

**Phụ thuộc ngữ cảnh:**

| Loại | Số turn | % |
| :--- | ---: | ---: |
| standalone | 38 | 50.67% |
| pronoun | 33 | 44.0% |
| connector | 4 | 5.33% |
| short_ellipsis | 0 | 0% |

→ **67.27%** turn sau turn đầu cần rewrite.
- Turn đầu có đại từ/liên từ lơ lửng: 1 (5.0%)
- Chuyển chủ đề: {'on_topic': 43.64, 'weak': 34.55, 'shift': 21.82} | hội thoại nhảy chủ đề ≥50% turn: 20.0%

**Loại câu hỏi:** yes_no 46.67%, statement_other 42.67%, what 6.67%, social 1.33%, how 1.33%, wh_other 1.33%

## 6. Gold / qrels

- Nguồn gold: {'inline': 75} | qrels được dùng để eval: False
- Gold/turn: mean 1.96, max 8
- Turn không gold: **0** (0.0%)
- Gold mồ côi: **0** cặp (0.0%), 0 doc
- qrels: khớp 75/75 qid | mồ côi **0** (0.0%) | gold inline ≠ qrels: **0** turn
- Doc chưa từng là gold: 61,892/61,961 (99.89%) | Gini 0.263
- Độ dài gold vs corpus (median): 1724.0 vs 81.0 (tỷ lệ 21.28x)
- Gold có lỗi nghiêm trọng: 14.49% | false-negative tiềm năng: 0 (0.0%) | gold trùng nhau: 0

## 7. Liên kết query ↔ gold

- Lexical overlap: mean **0.303** (có history: 0.28) | overlap=0: 4.0% | <20%: 29.33% | overlap=0 dù có history: 0.0%
- Overlap theo ngữ cảnh: {'standalone': 0.356, 'pronoun': 0.244, 'connector': 0.282}
- OOV: 12.0% (TB 1.18%)
- **Vị trí bằng chứng** (75 mẫu): {'0-20%': 44.0, '20-40%': 18.67, '40-60%': 8.0, '60-80%': 20.0, '80-100%': 9.33} | median offset 282c | sau 650c: 30.67% | sau 512 token: 0.0%

## 8. BM25 baseline

- 75 query | 69 gold + 200 nhiễu
- nDCG@10 single/history = 0.5593/0.7894 | Recall@10 = 0.7465/0.9275

**Vị trí turn:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | 20 | 0.7017 | 0.6943 | 0.8938 | 0.85 |
| 2 | 20 | 0.5986 | 0.8334 | 0.7506 | 0.9256 |
| 3 | 20 | 0.5358 | 0.8348 | 0.75 | 0.9875 |
| 4 | 12 | 0.3211 | 0.8698 | 0.4667 | 0.9833 |
| 5+ | 3 | 0.4582 | 0.5064 | 0.8333 | 0.8333 |

**Ngữ cảnh:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| connector | 4 | 0.5 | 0.8885 | 0.5 | 0.95 |
| pronoun | 33 | 0.3958 | 0.8144 | 0.5564 | 0.9549 |
| standalone | 38 | 0.7076 | 0.7574 | 0.9375 | 0.9013 |

**Loại câu hỏi:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| how | 1 | 0.0 | 1.0 | 0.0 | 1.0 |
| social | 1 | 1.0 | 1.0 | 1.0 | 1.0 |
| statement_other | 32 | 0.6168 | 0.7586 | 0.7751 | 0.8717 |
| wh_other | 1 | 0.5 | 1.0 | 1.0 | 1.0 |
| what | 5 | 0.6118 | 0.7091 | 1.0 | 0.9 |
| yes_no | 35 | 0.5044 | 0.8111 | 0.691 | 0.9762 |

**Chuyển chủ đề:**

| Nhóm | n | nDCG single | nDCG history | R@10 single | R@10 history |
| :--- | ---: | ---: | ---: | ---: | ---: |
| n/a | 20 | 0.7017 | 0.6943 | 0.8938 | 0.85 |
| on_topic | 24 | 0.5396 | 0.8349 | 0.7056 | 0.9861 |
| shift | 12 | 0.463 | 0.7364 | 0.5982 | 0.8524 |
| weak | 19 | 0.4953 | 0.8656 | 0.7368 | 0.9825 |

- Turn khó: **1** (1.33%) — {'ranking/distractor': 1}

## 9. Rò rỉ giữa các split

| Split | Turn | Query trùng dev | Query gần-trùng dev | Gold chung dev |
| :--- | ---: | ---: | ---: | ---: |
| train | 184 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |

## 10. Giới hạn

- Cờ nội dung là HEURISTIC (regex, tỷ lệ stopword) → có dương tính giả.
- Gần trùng: MinHash trên 5-word shingle, tối đa 1500 shingle đầu.
- Phụ thuộc ngữ cảnh / loại câu hỏi dựa trên regex tiếng Anh.
- Vị trí bằng chứng dựa trên trùng từ khóa (không phải đánh giá câu trả lời thật).
- BM25 chạy trên corpus con: chỉ so sánh tương đối.
- Health score là chỉ báo thô; hệ số trừ nằm trong `compute_health()`.

## 11. Ví dụ lỗi chi tiết

*Mỗi loại lỗi liệt kê tối đa `--examples` ví dụ; loại không có lỗi được đánh dấu ✅.*
## A. Toàn vẹn cấu trúc

### ✅ File bị thiếu
- Không phát hiện.

### ✅ Dòng JSON lỗi / không phải object
- Không phát hiện.

### ✅ Doc thiếu trường id
- Không phát hiện.

### ✅ doc_id trùng
- Không phát hiện.

### ✅ Doc thiếu trường text
- Không phát hiện.

### ✅ Trường text sai kiểu (không phải string)
- Không phát hiện.

### ✅ Trường title rỗng/sai
- Không phát hiện.

### ✅ qrels: dòng sai format
- Không phát hiện.

### ✅ qrels: cặp (qid, doc) trùng
- Không phát hiện.

### ✅ qrels: relevance ≤ 0
- Không phát hiện.

### ✅ Benchmark: conversation_id trùng
- Không phát hiện.

### ✅ Benchmark: hội thoại rỗng
- Không phát hiện.

### ✅ Benchmark: role không xen kẽ
- Không phát hiện.

### ✅ Benchmark: turn thiếu query
- Không phát hiện.

## B. Chất lượng nội dung tài liệu

### ✅ `empty` — tài liệu rỗng
- Không phát hiện.

### ❌ `too_short` — quá ngắn (<50 ký tự) — 24,256

**`Odometry/23051_0.txt`** (34 ký tự)
```text
[ The Construct ROS Community ](/)
```
**`Odometry/23051_13.txt`** (39 ký tự)
```text
Hi [ @w.ronaldo.cd ](/u/w.ronaldo.cd) ,
```
**`Odometry/23051_17.txt`** (17 ký tự)
```text
Regards, Girish
```
**`Odometry/23051_26.txt`** (18 ký tự)
```text
It continues with:
```
**`Odometry/23051_29.txt`** (39 ký tự)
```text
Hi [ @w.ronaldo.cd ](/u/w.ronaldo.cd) ,
```

### ❌ `mojibake` — lỗi encoding (mojibake) — 189

**`takeoff_rotation/transformationshtml_11.txt`** (1160 ký tự)
```text
>>> q1[3] == q0[3] and all(q1[:3] == -q0[:3]) True ` tf.transformations. ` ` quaternion_from_euler ` ( _ai_ , _aj_ , _ak_ , _axes='sxyz'_ ) Â¶ Return quaternion from Euler angles and axis sequence. ai, aj, ak : Euler’s r…
```
**`takeoff_rotation/transformationshtml_7.txt`** (1259 ký tự)
```text
Return Euler angles from quaternion for specified axis sequence. >>> angles = euler_from_quaternion([0.06146124, 0, 0, 0.99810947]) >>> numpy.allclose(angles, [0.123, 0, 0]) True ` tf.transformations. ` ` euler_matrix ` …
```
**`teleopanel/panelplugintutorialh_24.txt`** (135 ký tự)
```text
Building the Plugin Â¶ To build the plugin, just do the normal “rosmake” thing: rosmake rviz_plugin_tutorials
```
**`teleopanel/panelplugintutorialh_25.txt`** (1383 ký tự)
```text
Exporting the Plugin Â¶ For the plugin to be found and understood by other ROS packages (in this case, rviz), it needs a “plugin_description.xml” file. This file can be named anything you like, as it is specified in the …
```
**`teleopanel/panelplugintutorialh_28.txt`** (1315 ký tự)
```text
Trying It Out Â¶ Once your RViz plugin is compiled and exported, simply run rviz normally: rosrun rviz rviz and rviz will use pluginlib to find all the plugins exported to it. Add a Teleop panel by opening the “Panels” m…
```

### ❌ `control_chars` — ký tự điều khiển — 74

**`gz_sim/edit_45.txt`** (613 ký tự)
```text
$ gz sim --help Environment variables: GZ_SIM_RESOURCE_PATH Colon separated paths used to locate resources such as worlds and models. GZ_SIM_SYSTEM_PLUGIN_PATH Colon separated paths used to locate system plugins. GZ_SIM_…
```
**`automap_project/hornung13auropdf_22.txt`** (980 ký tự)
```text
10 ·10−3 Resolution [m] Time [ms] Freiburg campus Freiburg campus, trunc. FR-079 corridor FR-079 corridor, trunc. Fig. 16 Average time to update an octree map by inserting one data point for the datasets Freiburg campus …
```
**`automap_project/hornung13auropdf_7.txt`** (1478 ký tự)
```text
is estimated according to P(n | z1:t) = (1)  1+ 1−P(n | zt) P(n | zt) 1−P(n | z1:t−1) P(n | z1:t−1) P(n) 1−P(n) −1 This update formula depends on the current measurement zt , a prior probability P(n), and the previous …
```
**`crazy_file_add_variable/Report2020Undergradu_31.txt`** (1171 ký tự)
```text
extremely noisy and will be inaccurate [2, 11]. To accurately stabilise the position of the Crazyflie, it is required for additional sensors to perform measurements relative to the external environment [16]. 20 Motor Dri…
```
**`crazy_file_add_variable/Report2020Undergradu_32.txt`** (2504 ký tự)
```text
=  T 0.0065K/m 1 −  p 101325Pa 0.19026 (15) Where zsea, altitude relative to sea level, m; T, temperature, K (if this cannot be measured, T0 as the temperature at the lower troposphere limit may be used, 288.15K); …
```

### ❌ `html_residue` — HTML/entity còn sót — 44

**`roslib_message/ros2actionclienthtml_0.txt`** (1553 ký tự)
```text
<!DOCTYPE html> <html> <head> <meta charset="utf-8" /> <script src="https://unpkg.com/eventemitter3@latest/dist/eventemitter3.umd.min.js"></script> <script src="../dist/RosLib.umd.cjs"></script> <script> // Connecting to…
```
**`roslib_message/ros2actionclienthtml_1.txt`** (1101 ký tự)
```text
}); // Send an action goal var goal = {order: 5}; var goal_id = fibonacciClient.sendGoal(goal, function(result) { console.log('Result for action goal on ' + fibonacciClient.name + ': ' + result.result.sequence); }, funct…
```
**`visual_marker/visualservoingingaze_6.txt`** (889 ký tự)
```text
<visual name="visual"> <pose>0 0 0 0 0 0</pose> <geometry> <box> <size>0.0001 0.15 0.15</size> </box> </geometry> <material> <script> <uri>model://aruco_marker/materials/scripts</uri> <uri>model://aruco_marker/materials/…
```
**`crazy_file_add_variable/incorrectbatteryvolt_50.txt`** (9 ký tự)
```text
* &nbsp;
```
**`crazy_file_add_variable/incorrectbatteryvolt_51.txt`** (9 ký tự)
```text
* &nbsp;
```

### ❌ `boilerplate` — boilerplate/menu/footer — 866

**`gazebo_plugin/MulticopterVelocityC1_5.txt`** (1302 ký tự)
```text
this->noiseParameters.angularVelocityMean = math::eigen3::convert(angularVelocityMean); this->noiseParameters.angularVelocityStdDev = math::eigen3::convert(angularVelocityStdDev); if (sdfClone->HasElement("robotNamespace…
```
**`odometry_trajectory/PlotJuggler_79.txt`** (824 ký tự)
```text
Data sources (file and streaming) * Load CSV files. * Load [ ULog ](https://dev.px4.io/v1.9.0/en/log/ulog_file_format.html) (PX4). * Subscribe to many different streaming sources: MQTT, WebSockets, ZeroMQ, UDP, etc. * Un…
```
**`odom_transform/WritingATf2Broadcast_12.txt`** (1490 ký tự)
```text
#include "geometry_msgs/msg/transform_stamped.hpp" #include "rclcpp/rclcpp.hpp" #include "tf2/LinearMath/Quaternion.h" #include "tf2_ros/transform_broadcaster.h" #include "turtlesim/msg/pose.hpp" class FramePublisher : p…
```
**`point_cloud/pclros_93.txt`** (526 ký tự)
```text
Examples Subscribe to the ` /velodyne/pointcloud2 ` topic and save each message in the current directory. File names look like ` 1285627014.833100319.pcd ` , the exact names depending on the message time stamps. $ rosrun…
```
**`Odometry/23051_52.txt`** (233 ký tự)
```text
* [ Home ](/) * [ Categories ](/categories) * [ FAQ/Guidelines ](/guidelines) * [ Terms of Service ](http://www.theconstructsim.com/terms_and_conditions/) * [ Privacy Policy ](http://www.theconstructsim.com/privacy_polic…
```

### ❌ `url_heavy` — URL chiếm >25% nội dung — 6,878

**`odometry_trajectory/PlotJuggler_82.txt`** (792 ký tự)
```text
Supported plugins Some plugins can be found in a different repository. The individual README files _should_ include all the information needed to compile and use the plugin. Please submit specific issues, Pull Requests a…
```
**`odometry_trajectory/PlotJuggler_84.txt`** (855 ký tự)
```text
Snap (recommended in Ubuntu, to ROS users too) The snap contains a version of PlotJuggler that can work with either ROS1 or ROS2. [ ![Get it from the Snap Store](https://camo.githubusercontent.com/46aa03c94aa80f6545e01f2…
```
**`hardware_control/1240_31.txt`** (2124 ký tự)
```text
Thanks for explaining it. Is this restriction at the loaned interfaces level already applied to the code in this PR? Sorry, something went wrong. All reactions [ ![christophfroehlich](https://avatars.githubusercontent.co…
```
**`rosgzbridge/humble_9.txt`** (2626 ký tự)
```text
# Integration between ROS and Gazebo ## Packages This repository holds packages that provide integration between [ ROS ](http://www.ros.org/) and [ Gazebo ](https://gazebosim.org) : * [ ros_gz ](https://github.com/gazebo…
```
**`ros2_driver/ros2ousterdrivers_22.txt`** (903 ký tự)
```text
ROS2 Ouster Drivers These are an implementation of ROS2 drivers for the Ouster lidar. This includes all models of the OS-x from 16 to 128 beams running the firmware 2.2-2.4. You can find a few videos looking over the sen…
```

### ❌ `symbol_heavy` — ký hiệu lạ >30% — 2,705

**`Odometry/allp2html_114.txt`** (5 ký tự)
```text
* * *
```
**`Odometry/allp2html_187.txt`** (5 ký tự)
```text
* * *
```
**`Odometry/allp2html_237.txt`** (5 ký tự)
```text
* * *
```
**`Odometry/allp2html_240.txt`** (5 ký tự)
```text
* * *
```
**`Odometry/allp2html_241.txt`** (5 ký tự)
```text
* * *
```

### ❌ `repetitive` — lặp từ/dòng bất thường — 1,400

**`ros2cpp/navigationlaunchpy_20.txt`** (1667 ký tự)
```text
executable='waypoint_follower', name='waypoint_follower', output='screen', respawn=use_respawn, respawn_delay=2.0, parameters=[configured_params], arguments=['--ros-args', '--log-level', log_level], remappings=remappings…
```
**`number_commands/differentupdaterates_11.txt`** (383 ký tự)
```text
> desired_hw_update_rate_ == 0 || > ((update_loop_counter_ % desired_hw_update_rate_) == > 0); > > if (hardware_go){ > // hardware comms and operations > ... > } > ... > > // update counter > ++update_loop_counter_; > up…
```
**`robot_stop/usingcollisionmonito_530.txt`** (222 ký tự)
```text
polygons: ["PolygonStop", "PolygonSlow"] PolygonStop: type: "polygon" points: "[[0.4, 0.3], [0.4, -0.3], [0.0, -0.3], [0.0, 0.3]]" action_type: "stop" min_points: 4
```
**`robot_stop/usingcollisionmonito_534.txt`** (893 ký tự)
```text
VelocityPolygonStop: type: "velocity_polygon" action_type: "stop" min_points: 6 visualize: True enabled: True polygon_pub_topic: "velocity_polygon_stop" velocity_polygons: ["rotation", "translation_forward", "translation…
```
**`Odometry/allp2html_142.txt`** (2208 ký tự)
```text
F5&, F6&, F7&, F8&) [with F0 = message_filters::Subscriber<:featurebarray_>>>, F1 = message_filters::Subscriber<:odometry_>>>, F2 = message_filters::NullFilter<:nulltype>, F3 = message_filters::NullFilter<:nulltype>, F4 …
```

### ❌ `non_english` — nghi không phải tiếng Anh — 10,167

**`ros2cpp/navigationlaunchpy_20.txt`** (1667 ký tự)
```text
executable='waypoint_follower', name='waypoint_follower', output='screen', respawn=use_respawn, respawn_delay=2.0, parameters=[configured_params], arguments=['--ros-args', '--log-level', log_level], remappings=remappings…
```
**`costmap_subscript/nav2costmap2d2Fplugi_14.txt`** (166 ký tự)
```text
map_sub_ = node->create_subscription<nav_msgs::msg::OccupancyGrid>( map_topic_, map_qos, std::bind(&StaticLayer::incomingMap, this, std::placeholders::_1));
```
**`gazebo_plugin/MulticopterVelocityC1_2.txt`** (1426 ký tự)
```text
loadRotorConfiguration(_ecm, sdfClone->GetElement("rotorConfiguration"), this->model, this->comLinkEntity); // DEBUG // std::cout << "Found " // << vehicleParams.rotorConfiguration.size() // << " rotors" << std::endl; //…
```
**`image_callback/AboutExecutorshtml_10.txt`** (646 ký tự)
```text
Types of Executors ï Currently, rclcpp provides three Executor types, derived from a shared parent class: ![digraph Flatland { Executor -> SingleThreadedExecutor \[dir = back, arrowtail = empty\]; Executor -> MultiThre…
```
**`arduino/ros2serialinterface_7.txt`** (1500 ký tự)
```text
serial_server_launch.py: terminal_key_pub.py: virtual_serial_client.py: virtual_serial_server.py: virtual_serial_setup.py: ## Running these files To run predef_timed_pub.py: ` ros2 run ros2_serial_interface predef_timed_…
```

### ❌ `pii_email` — chứa email — 209

**`nv_planner/230715236pdf_0.txt`** (1609 ký tự)
```text
From the Desks of ROS Maintainers: A Survey of Modern & Capable Mobile Robotics Algorithms in the Robot Operating System 2 Steve Macenski ROS 2 Project Lead Samsung Research s.macenski@samsung.com Tom Moore Robot Localiz…
```
**`rosgzbridge/humble_10.txt`** (1608 ký tự)
```text
mkdir -p ~/ws/src cd ~/ws/src # Download needed software git clone https://github.com/gazebosim/ros_gz.git -b humble 2. Install dependencies (this may also install Gazebo): cd ~/ws rosdep install -r --from-paths src -i -…
```
**`rosdep_install/1478_3.txt`** (1752 ký tự)
```text
## Bug report My robot needs a lot of Adafruit and Sparkfun sensors and I am experimenting installing new drivers into my ROS2 humble installtion. rosdistro was forked and imported and python.yaml adjusted accordingly. T…
```
**`access_urdf/myroboticmanipulator_111.txt`** (53 ký tự)
```text
[ info@theconstruct.ai ](mailto:info@theconstruct.ai)
```
**`bounding_box_rviz/moveitvisualtools_8.txt`** (4276 ký tự)
```text
](https://camo.githubusercontent.com/62176a685c40980602f2dfd8f0156f913b525c3564d8e11ef415621eadd9e8d4/68747470733a2f2f7069636b6e696b2e61692f6173736574732f696d616765732f6c6f676f2e6a7067) This open source project was devel…
```

### ❌ `pii_phone` — chứa số điện thoại — 60

**`access_urdf/myroboticmanipulator_112.txt`** (17 ký tự)
```text
(+34) 687 672 123
```
**`ackermann/interfacecontrolchec_34.txt`** (89 ký tự)
```text
The platform computer is on the 192.168.131.xxx subnet (ideally in the range 1-4). |
```
**`automap_project/hornung13auropdf_0.txt`** (2762 ký tự)
```text
Autonomous Robots (2013) Preprint, final version available at DOI 10.1007/s10514-012-9321-0 OctoMap: An Efficient Probabilistic 3D Mapping Framework Based on Octrees Armin Hornung · Kai M. Wurm · Maren Bennewitz · Cyrill…
```
**`automap_project/hornung13auropdf_13.txt`** (2673 ký tự)
```text
current implementation. This enables fast tree traversals by using computable voxel addresses. However, the depth limit also poses a limit on the maximum spatial extent of the octree. At a resolution of 1 cm, for example…
```
**`automap_project/hornung13auropdf_20.txt`** (913 ký tự)
```text
0 50 100 Scan number Memory [MB] FR-079 corridor (5 cm res.) Full 3D grid No compression Octree compression ML octree compression 20 40 60 80 0 200 400 600 Scan number Memory [MB] Freiburg campus (20 cm res.) Full 3D gri…
```

### ❌ `possibly_truncated` — nghi bị cắt cụt (không dấu câu cuối) — 8,069

**`gazebo/indexhtml_1.txt`** (2900 ký tự)
```text
This is a ROS 2 package for integrating the _ros2_control_ controller architecture with the [ Gazebo Classic ](https://classic.gazebosim.org/) simulator. This package provides a Gazebo plugin which instantiates a _ros2_c…
```
**`costmap_subscript/nav2costmap2d2Fplugi_15.txt`** (316 ký tự)
```text
if (subscribe_to_updates_) { RCLCPP_INFO(logger_, "Subscribing to updates"); map_update_sub_ = node->create_subscription<map_msgs::msg::OccupancyGridUpdate>( map_topic_ + "_updates", rclcpp::SystemDefaultsQoS(), std::bin…
```
**`launch_moveit/b634e96c2f080ab38780_5.txt`** (1938 ký tự)
```text
[ View file ](/ros- planning/moveit2/blob/b634e96c2f080ab38780668e85e974351978106d/moveit_configs_utils/moveit_configs_utils/launches.py) Edit file Delete file [ Open in desktop ](https://desktop.github.com) This file co…
```
**`gazebo_plugin/MulticopterVelocityC1_1.txt`** (1430 ký tự)
```text
////////////////////////////////////////////////// void MulticopterVelocityControl::Configure(const Entity &_entity, const std::shared_ptr<const sdf::Element> &_sdf, EntityComponentManager &_ecm, EventManager &/*_eventMg…
```
**`gazebo_plugin/MulticopterVelocityC1_2.txt`** (1426 ký tự)
```text
loadRotorConfiguration(_ecm, sdfClone->GetElement("rotorConfiguration"), this->model, this->comLinkEntity); // DEBUG // std::cout << "Found " // << vehicleParams.rotorConfiguration.size() // << " rotors" << std::endl; //…
```

### ❌ `starts_lower` — bắt đầu bằng chữ thường — 7,544

**`ros2cpp/navigationlaunchpy_20.txt`** (1667 ký tự)
```text
executable='waypoint_follower', name='waypoint_follower', output='screen', respawn=use_respawn, respawn_delay=2.0, parameters=[configured_params], arguments=['--ros-args', '--log-level', log_level], remappings=remappings…
```
**`costmap_subscript/nav2costmap2d2Fplugi_14.txt`** (166 ký tự)
```text
map_sub_ = node->create_subscription<nav_msgs::msg::OccupancyGrid>( map_topic_, map_qos, std::bind(&StaticLayer::incomingMap, this, std::placeholders::_1));
```
**`costmap_subscript/nav2costmap2d2Fplugi_15.txt`** (316 ký tự)
```text
if (subscribe_to_updates_) { RCLCPP_INFO(logger_, "Subscribing to updates"); map_update_sub_ = node->create_subscription<map_msgs::msg::OccupancyGridUpdate>( map_topic_ + "_updates", rclcpp::SystemDefaultsQoS(), std::bin…
```
**`gazebo_plugin/MulticopterVelocityC1_2.txt`** (1426 ký tự)
```text
loadRotorConfiguration(_ecm, sdfClone->GetElement("rotorConfiguration"), this->model, this->comLinkEntity); // DEBUG // std::cout << "Found " // << vehicleParams.rotorConfiguration.size() // << " rotors" << std::endl; //…
```
**`gazebo_plugin/MulticopterVelocityC1_5.txt`** (1302 ký tự)
```text
this->noiseParameters.angularVelocityMean = math::eigen3::convert(angularVelocityMean); this->noiseParameters.angularVelocityStdDev = math::eigen3::convert(angularVelocityStdDev); if (sdfClone->HasElement("robotNamespace…
```

### ❌ Trùng chính xác — 21,530

*4213 nhóm*

- nhóm: `galactic_ros/targetsetuphtml_38.txt`, `ros2humble/WindowsInstallBinary_118.txt`
```text
ros2 run demo_nodes_py listener
```
- nhóm: `imu_gazebo/specelemsensor_382.txt`, `imu_gazebo/specelemsensor_43.txt`
```text
##### degrees Attribute
```
- nhóm: `odom_transform/721_124.txt`, `odom_transform/721_151.txt`, `odom_transform/721_189.txt`, `odom_transform/721_98.txt`, `odom_transform/960_104.txt`, `odom_transform/960_73.txt`
```text
[ ![@matlabbe](https://avatars.githubusercontent.com/u/2319645?s=80&v=4) ](/matlabbe)
```
- nhóm: `prismatic_join/406_382.txt`, `set_position_ros2/106_239.txt`
```text
Multiple requests from the same IP address are counted as one view.
```
- nhóm: `ros_convert/717_294.txt`, `ros_convert/717_308.txt`
```text
**[ danthony06 ](/danthony06) ** commented Apr 9, 2021
```

### ❌ Gần trùng (khác nhau chút ít) — 182

*MinHash — doc cùng cụm nhưng nội dung không giống hệt*


## C. Hội thoại / query

### ✅ Query rỗng
- Không phát hiện.

### ✅ Query trùng nhau
- Không phát hiện.

### ✅ Query quá ngắn (≤ 2 từ)
- Không phát hiện.

### ✅ Query quá dài (> 60 từ)
- Không phát hiện.

### ❌ Turn đầu có đại từ/liên từ lơ lửng — 1

- `82_turn_1`: In ROS, is it possible to use multiple dynamic reconfigure servers for different sensor namespaces in one node?

### ❌ Turn phụ thuộc ngữ cảnh — đại từ (cần rewrite) — 33

- `2_turn_3`: Is that error more about Gazebo not finding the plugin, or could it be something with how the plugin starts up?
- `15_turn_4`: Is there anything tricky about updating the launch files, or does the Migration Guide make it pretty straightforward?
- `16_turn_2`: I wonder if there’s an official write-up or guide from the main Nav2 developers that lays all this out?
- `16_turn_3`: Have there been any recent papers in Robotics and Autonomous Systems comparing those Nav2 planners and controllers?
- `16_turn_4`: Is there an easy way to compare all those planners and controllers side by side?

### ❌ Turn phụ thuộc ngữ cảnh — liên từ (cần rewrite) — 4

- `32_turn_2`: Oh, and how do you pick the right topic name so the box shows up where you want in RVIZ?
- `32_turn_3`: And how do you actually tell rviz_visual_tools which topic to use for the bounding box marker?
- `46_turn_2`: Oh, what actually changed in the rolling release to let hardware get the original URDF now?
- `59_turn_4`: Oh, so does picking a different clock type when you make the node actually change what you get from node->now()?

### ✅ Turn phụ thuộc ngữ cảnh — câu ngắn/tỉnh lược (cần rewrite)
- Không phát hiện.

### ❌ Nhảy chủ đề đột ngột giữa 2 turn liền kề — 12

- `2_turn_2` (cos=0.0)
  - trước: In gazebo_ros2_control setup, does installing it with apt usually require extra steps for Gazebo to find plugins and con…
  - sau: Have you tried running the default demo to see if the plugin loads without any tweaks?
- `20_turn_2` (cos=0.0)
  - trước: In ROS 2 control, is there a way to pass custom data types between the hardware interface and the controller?
  - sau: Any idea when those changes from PR 1240 might actually land and start making a difference?
- `20_turn_3` (cos=0.0)
  - trước: Any idea when those changes from PR 1240 might actually land and start making a difference?
  - sau: Would that make it possible to just pass a whole custom class for joint states, then?
- `55_turn_4` (cos=0.0)
  - trước: Did you ever try installing the demo using the debian packages instead of building it from source?
  - sau: Is it possible one of the dependencies just didn’t get picked up by rosdep or apt?
- `59_turn_4` (cos=0.0)
  - trước: Is there a particular reason timers in ROS 2 rely on steady time instead of system or ROS time?
  - sau: Oh, so does picking a different clock type when you make the node actually change what you get from node->now()?

## D. Gold / qrels

### ✅ Gold mồ côi (doc không có trong corpus)
- Không phát hiện.

### ✅ qrels qid không khớp turn nào
- Không phát hiện.

### ✅ Gold inline (benchmark) ≠ qrels
- Không phát hiện.

### ✅ Turn không có gold
- Không phát hiện.

### ❌ Gold doc có lỗi nội dung nghiêm trọng — 10

- `ros2cpp/navigationlaunchpy_20.txt` ['repetitive', 'non_english']
```text
executable='waypoint_follower', name='waypoint_follower', output='screen', respawn=use_respawn, respawn_delay=2.0, parameters=[configured_params], arguments=['--ros-args', '--log-level', log_level], r…
```
- `hardware_control/1240_31.txt` ['url_heavy']
```text
Thanks for explaining it. Is this restriction at the loaned interfaces level already applied to the code in this PR? Sorry, something went wrong. All reactions [ ![christophfroehlich](https://avatars.…
```
- `hardware_control/1240_34.txt` ['non_english']
```text
controls/ros2_control/pull/1240/commits/667892dcb4cc0a6267d443b1add559f241ec8c3f "first steps towards variants and storing of value in handle, missing: * variant * adjusting of resource manager") ` … …
```
- `navsetplugin/sphericalcoordinates_1.txt` ['non_english']
```text
--> <sdf version="1.6"> <world name="spherical_coordinates"> <!-- Processes the NavSat sensor --> <plugin filename="ignition-gazebo-navsat-system" name="ignition::gazebo::systems::NavSat"> </plugin> <…
```
- `ros2_dependency/indexhtml_12.txt` ['non_english']
```text
Build from source  * Download all repositories mkdir -p ~/ros2_ws/src cd ~/ros2_ws/src git clone https://github.com/ros-controls/ros2_control_demos cd ~/ros2_ws/ vcs import src < src/ros2_control_dem…
```

### ✅ Gold có bản gần trùng KHÔNG phải gold (false-negative tiềm năng)
- Không phát hiện.

## E. Liên kết query ↔ gold

### ❌ Query không chia sẻ từ nào với gold — 3

- `72_turn_2` (pronoun) gold=['crazyswarm/usagehtmlcrazyfliesy_4.txt']: Could it just be that the parameter wants a different type, like maybe a boolean instead of an integer?
- `72_turn_3` (pronoun) gold=['crazyswarm/usagehtmlcrazyfliesy_4.txt']: Is it possible that parameter just can’t be changed after the node starts up?
- `100_turn_2` (pronoun) gold=['relative_path/PackagesClientLibrar_6.txt']: Is there an easy way to double-check if my package name matches everywhere it needs to?

### ❌ Bằng chứng nằm muộn (> 1500 ký tự) — 10

- `47_turn_2` offset=2314c gold=`prismatic_join/userdochtml_1.txt`
  - query: If you let both position and velocity commands through for that axis, could they end up conflicting or making the motion…
  - bằng chứng: * For ` velocity ` ( ` effort ` ) command interfaces, the position+velocity trajectory following error is mapped to ` velocity ` ( ` effort ` ) commands through…
- `47_turn_3` offset=2314c gold=`prismatic_join/userdochtml_1.txt`
  - query: Is it okay if the state interface only reports position, or does the controller really need velocity too for it to work …
  - bằng chứng: * For ` velocity ` ( ` effort ` ) command interfaces, the position+velocity trajectory following error is mapped to ` velocity ` ( ` effort ` ) commands through…
- `2_turn_2` offset=2175c gold=`gazebo/indexhtml_2.txt`
  - query: Have you tried running the default demo to see if the plugin loads without any tweaks?
  - bằng chứng: By default, without a ` <plugin> ` tag, _gazebo_ros2_control_ will attempt to
- `16_turn_1` offset=1871c gold=`nv_planner/230715236pdf_10.txt`
  - query: In ROS 2 navigation, is there a good overview comparing the main planners and controllers and their strengths?
  - bằng chứng: trajectory planners available in the broader ROS 2 ecosystem,
- `82_turn_1` offset=1698c gold=`dynamic_reconfig/dwaplannerroscpp_2.txt`
  - query: In ROS, is it possible to use multiple dynamic reconfigure servers for different sensor namespaces in one node?
  - bằng chứng: dsrv_ = new dynamic_reconfigure::Server<DWAPlannerConfig>(private_nh);

### ❌ Query chứa từ không có trong từ vựng corpus (OOV) — 9

- `72_turn_1` OOV=['cf231', 'setups']: In ROS2 Crazyswarm setups, how should the crazyflies.yaml file list 'cf231' so I can set its parameters?
- `2_turn_2` OOV=['tweaks']: Have you tried running the default demo to see if the plugin loads without any tweaks?
- `47_turn_2` OOV=['conflicting']: If you let both position and velocity commands through for that axis, could they end up conflicting or making the motion less smooth?
- `47_turn_4` OOV=['tries']: What happens if the controller tries to send a position past the axis’s software limits—does it just ignore it, or is there some error?
- `50_turn_2` OOV=['picks']: Is there a specific way to set both mu and mu2 in the <gazebo> tag so Gazebo actually picks them up?

## F. Turn khó với BM25 (recall@10 = 0)

### ❌ Turn khó — 1

*nguyên nhân: {'ranking/distractor': 1}*

- `20_turn_1` ti=0 ctx=standalone overlap=0.5: In ROS 2 control, is there a way to pass custom data types between the hardware interface and the controller?
  - gold ['hardware_control/1240_29.txt', 'hardware_control/1240_3.txt', 'hardware_control/1240_31.txt'] | top3 ['prismatic_join/userdochtml_1.txt', 'gazebo/indexhtml_2.txt', 'gazebo/indexhtml_3.txt']

## G. Rò rỉ giữa các split

### ✅ Split `train`: query trùng hệt với dev
- Không phát hiện.

### ✅ Split `train`: query gần trùng dev (Jaccard ≥ 0.9)
- Không phát hiện.

### ✅ Split `train`: gold doc dùng chung với dev
- Không phát hiện.