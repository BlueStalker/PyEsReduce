cd ..
rm -rf go.tar ./refine
mkdir refine
cp -r ./PyEsReduce/* ./refine
COPYFILE_DISABLE=1 tar vcf go.tar ./refine/
#ssh -t -i AWSKerrigan.pem ubuntu@54.88.9.158 "cd /home/ubuntu/; rm -rf go.tar"
scp -i AWSKerrigan.pem go.tar ubuntu@54.89.192.31:/home/ubuntu/
ssh -t -i AWSKerrigan.pem ubuntu@54.89.192.31 "sudo rm -rf /root/backup/*; sudo cp -r /root/refine/jobs /root/backup/; sudo cp /root/refine/port.config /root/backup/port.config; sudo rm -rf /root/refine; sudo cp -r /home/ubuntu/go.tar /root/; sudo tar vxf /root/go.tar -C /root/; sudo rm -rf /root/refine/jobs/; sudo cp -r /root/backup/jobs/ /root/refine; sudo cp /root/backup/port.config /root/refine/port.config;"

ssh -t -i AWSKerrigan.pem ubuntu@54.89.192.31 'bash -c "sudo cd /root/refine/; sudo ./server_cleanup.sh; sudo ./server_startup.sh"'
