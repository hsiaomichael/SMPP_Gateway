Installation Procedure .

Ack as SMPP Gateway 

1 : accept smpp client bind_tranceiver connection
2 : connect to remote SMSC with multi-smpp-connection (bind smpp_transciver)
3 : receive client submit_sm request and send to service(remote SMSC) using b-address binding
4 : receive remote SMSC deliver_sm request and send back to client

ps : deliver_sm request always send to latest smpp client connection

</br>
copy all files to same directory
</br>
Edit SMPPGateway.cfg (local/Remote ip , port , SMPP system_id/system_type/password  )
</br>
chmod +x run.sh
</br>./run.sh
  

