
# one for a server and a client

echo "127.0.0.1" > ifconfig.txt
echo "127.0.0.1" >> ifconfig.txt
echo "127.0.0.1" >> ifconfig.txt
echo "127.0.0.1" >> ifconfig.txt

export NODE_CNT=2
export CLIENT_NODE_CNT=2

# Verify the node count
line_count=$(wc -l < ifconfig.txt)
total_nodes=$((NODE_CNT + CLIENT_NODE_CNT))

if [ $line_count -eq $total_nodes ]; then
    echo "The number of lines in ifconfig.txt is correct."
else
    echo "Error: The number of lines in ifconfig.txt does not match the sum of NODE_CNT and CLIENT_NODE_CNT."
fi