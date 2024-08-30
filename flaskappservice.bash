[Unit]
Description=Flask Application

[Service]
Type=simple
WorkingDirectory=/home/ubuntu/reto1_top_telem/superpeer
ExecStart=/bin/bash -c "source /home/ubuntu/reto1_top_telem/myenv/bin/activate && exec python app.py"
StandardError=journal
Restart=always
User=ubuntu 

[Install]
WantedBy=multi-user.target
