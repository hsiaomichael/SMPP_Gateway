Installation Procedure .

Ack as SMPP Gateway , receive client SMPP request and forward to server:remote SMSC.
expected 1 client connection (response always send to latest client connection)
i.e. 1 client connection to multi-server connection (and using b-address binding )

ToDo : receive server delivery_sm request and send to client side

</br>
copy all files to same directory
</br>
Edit SMPPGateway.cfg (local/Remote ip , port , SMPP system_id/system_type/password  )
</br>
chmod +x run.sh
</br>./run.sh
  

