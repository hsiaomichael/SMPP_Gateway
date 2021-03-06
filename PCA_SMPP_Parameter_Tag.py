dest_addr_subunit = chr(0x00) + chr(0x05)
dest_network_type = chr(0x00) + chr(0x06)
dest_bearer_type = chr(0x00) + chr(0x07)
dest_telematics_id = chr(0x00) + chr(0x08)
source_addr_subunit = chr(0x00) + chr(0x0d)
source_network_type = chr(0x00) + chr(0x0e)
source_bearer_type = chr(0x00) + chr(0x0f)
source_telematics_id = chr(0x00) + chr(0x10)
qos_time_to_live = chr(0x00) + chr(0x17)
payload_type = chr(0x00) + chr(0x19)
additional_status_info_text = chr(0x00) + chr(0x1d)
receipted_message_id = chr(0x00) + chr(0x1e)
ms_msg_wait_facilities = chr(0x00) + chr(0x30)
privacy_indicator = chr(0x02) + chr(0x01)     
source_subaddress = chr(0x02) + chr(0x02)    
dest_subaddress = chr(0x02) + chr(0x03)     
user_message_reference = chr(0x02) + chr(0x04)
user_response_code = chr(0x02) + chr(0x05)
source_port = chr(0x02) + chr(0x0a)
destination_port = chr(0x02) + chr(0x0b)
sar_msg_ref_num = chr(0x02) + chr(0x0c)
language_indicator = chr(0x02) + chr(0x0d)   
sar_total_segments = chr(0x02) + chr(0x0e) 
sar_segment_seqnum = chr(0x02) + chr(0x0f)
SC_interface_version = chr(0x02) + chr(0x10)
callback_num_pres_ind = chr(0x03) + chr(0x02)
callback_num_atag = chr(0x03) + chr(0x03) 
number_of_messages = chr(0x03) + chr(0x04)  
callback_num = chr(0x03) + chr(0x81)           
dpf_result = chr(0x04) + chr(0x20) 
set_dpf = chr(0x04) + chr(0x21)  
ms_availability_status = chr(0x04) + chr(0x22) 
network_error_code = chr(0x04) + chr(0x23) 
message_payload = chr(0x04) + chr(0x24) 
delivery_failure_reason = chr(0x04) + chr(0x25)
more_messages_to_send = chr(0x04) + chr(0x26) 
message_state = chr(0x04) + chr(0x27) 
ussd_service_op = chr(0x05) + chr(0x01)
display_time  = chr(0x12) + chr(0x01)   
sms_signal = chr(0x12) + chr(0x03)
ms_validity = chr(0x12) + chr(0x04)     
alert_on_message_delivery = chr(0x13) + chr(0x0c)
its_reply_type = chr(0x13) + chr(0x80) 
its_session_info = chr(0x13) + chr(0x83) 


    
bind_receiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x01)
bind_receiver_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x01)
bind_transmitter = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x02)
bind_transmitter_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x02)
bind_transceiver = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x09)
bind_transceiver_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x09)


outbind = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x0b) 
unbind = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x06) 
unbind_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x06) 
submit_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x04) 
submit_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x04) 
deliver_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x05) 
deliver_sm_resp = chr(0x80)+chr(0x0)+chr(0x00)+chr(0x05) 	
query_sm = chr(0x00)+chr(0x00)+chr(0x00)+chr(0x03) 
query_sm_resp = chr(0x80)+chr(0x00)+chr(0x00)+chr(0x03) 
cancel_sm = chr(0x00)+chr(0x0)+chr(0x00)+chr(0x08) 
cancel_sm_resp =chr(0x80)+chr(0x0)+chr(0x00)+chr(0x08) 
replace_sm =  chr(0x00)+chr(0x0)+chr(0x00)+chr(0x07) 
replace_sm_resp=  chr(0x80)+chr(0x0)+chr(0x00)+chr(0x07) 
enquire_link =  chr(0x00)+chr(0x00)+chr(0x00)+chr(0x15) 
enquire_link_resp =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x15) 
generic_nack =  chr(0x80)+chr(0x00)+chr(0x00)+chr(0x00) 
    
    
    
command_id_dict = {}
command_id_dict[bind_receiver] = 'bind_receiver'
command_id_dict[bind_receiver_resp] = 'bind_receiver_resp'
command_id_dict[bind_transmitter] = 'bind_transmitter'
command_id_dict[bind_transmitter_resp] = 'bind_transmitter_resp'
command_id_dict[submit_sm] = 'submit_sm'
command_id_dict[submit_sm_resp] = 'submit_sm_resp'
command_id_dict[deliver_sm] = 'deliver_sm' 	
command_id_dict[deliver_sm_resp] = 'deliver_sm_resp'
command_id_dict[enquire_link] = 'enquire_link'
command_id_dict[enquire_link_resp] = 'enquire_link_resp'    
command_id_dict[unbind] = 'unbind'
command_id_dict[unbind_resp] = 'unbind_resp'    

command_id_dict[bind_transceiver] = 'bind_transceiver'
command_id_dict[bind_transceiver_resp] = 'bind_transceiver_resp'

