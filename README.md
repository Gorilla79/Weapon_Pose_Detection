# Weapon_Pose_Detection

[동작 원리]
1. 사람 객체의 포즈를 감지하고 사람 포즈(스켈레톤)의 양손 영역을 탐색
2. 양손 vertex 근처 20프레임 탐색 -> 무기가 탐지될 시 탐지 영역을 50프레임으로 확장
3. 무기 탐지 시 가장 인접한 손 vertex를 소지한 사람 객체를 targetting
4. 해당 사람 객체를 위험 인물(Dangerous Human)으로 판단

[기능]
- 사람, 무기 객체 인식
- 사람 포즈의 상체 스켈레톤 생성
- 컬러 이미지와 depth 이미지 표시
- 사람 및 무기 객체의 중심점 표시(컬러 이미지에서 중심점 확인, depth 이미지에도 동일한 중심점 좌표 표시_
- 컬러 이미지에서 마우스로 클릭을 하면 해당 지점의 depth값 표시
- 사람 및 무기, 위험 인물에 대한 바운딩 박스와 라벨링 표시

[사용 모델] </br>
사람 객체 : yolov8n.pt </br>
사람 포즈 : yolov8n-pose.pt </br>
망치 : best_hammer.pt </br>
칼 : best_knife.pt </br>
총 : best_gun.pt </br>
배트 : best_bet.pt </br>
도끼 : best_axe.pt </br>

[평가 지표]
| Model  | Epoch | Precision | Recall | mAP50 | mAP50-95 | Validation Box Loss | Validation Class Loss | Validation DFL Loss |
|--------|-------|-----------|--------|-------|----------|----------------------|-----------------------|---------------------|
| Hammer | 100   | 0.9007    | 0.8694 | 0.9296| 0.7130   | 0.8785               | 0.5505                | 1.0372              |
| Knife  | 100   | 0.9059    | 0.9034 | 0.9555| 0.7528   | 0.7997               | 0.5150                | 0.9982              |
| Gun    | 100   | 0.8799    | 0.8617 | 0.9160| 0.7012   | 0.8783               | 0.5748                | 1.0545              |
| Bat    | 100   | 0.8979    | 0.8801 | 0.9326| 0.7186   | 0.8638               | 0.5509                | 1.0298              |
| Axe    | 100   | 0.8970    | 0.8855 | 0.9395| 0.7242   | 0.8669               | 0.5383                | 1.0345              |

[실제 결과]
- hammer
![hammer_pose_detection](https://github.com/user-attachments/assets/7f9faa99-dd80-4804-9d12-683c0579984d)
![hammer_pose_detection(danger)](https://github.com/user-attachments/assets/53b1bf2a-2b17-4ee1-a07e-95bc7a1dfe20)

- knife
![knife_pose_detection](https://github.com/user-attachments/assets/0d95d73c-4776-4598-a124-d342ef9fb160)
![knife_pose_detection(danger)](https://github.com/user-attachments/assets/108e13f2-ad1e-40f5-aa66-6db517f48630)

- gun
![gun_pose_detection](https://github.com/user-attachments/assets/81062e68-db82-48d4-89ea-10ca70907cec)
![gun_pose_detection(danger)](https://github.com/user-attachments/assets/6baae84e-8d9a-4107-a2d6-773f53948588)

- bat
![bat_pose_detection](https://github.com/user-attachments/assets/eef0ee46-d561-4e60-8832-943a27edccb9)
![bat_pose_detection(danger)](https://github.com/user-attachments/assets/82189c85-1a9b-417e-ab52-e2e8905c5e11)

- axe</br>
결과가 좋지 않아 추후 개선 필요
