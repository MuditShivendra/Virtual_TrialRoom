# cd ../../3d-pose-baseline
# source venv/bin/activate
python3 ../3d-pose-baseline/src/openpose_3dpose_sandbox.py --camera_frame --residual --batch_norm --dropout 0.5 --max_norm --evaluateActionWise --use_sh --epochs 200 --load 4874200 --pose_estimation_json ../WeAR-Server/$1 --write_gif --gif_fps 24
