server {
    charset utf-8;
    listen 80;
    server_name home.io; 

    location /static { 
        alias /home/ubuntu/sites/hoome.io/backend_core/static; 
    }

    location / { 
        proxy_set_header Host $host;
        proxy_pass http://unix:/tmp/hoome.io.socket;
    }
	
	location ~* .(jpg|jpeg|png|gif|ico|css|js)$ {
		expires 365d;
	}

}