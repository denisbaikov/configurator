#!/bin/sh

if [ $# -eq 0 ]; then
        echo "Error"
        exit 1
fi

count_bracket=0
find_flag=false
index=0

arr_host_name=()
arr_host_mac=()
arr_host_ip=()


while read line
do
        if [[ $find_flag == true ]]; then
                start=`echo ${line:0:13}`
                if [[ $start == 'hardware ethe' ]]; then
                        mac=`echo $line | awk '{ print $3 }' | sed 's/[;]//'`
                        arr_host_mac[$index]=$mac
                fi

                if [[ $start == 'fixed-address' ]]; then
                        ip=`echo $line | awk '{ print $2 }' | sed 's/[;]//'`
                        arr_host_ip[$index]=$ip
                fi
        fi

        index_bracket=`expr index "$line" {`
        if [[ $index_bracket != 0 ]]; then
                count_bracket=`expr $count_bracket + 1`
                #echo 'index_bracket = '$index_bracket
        fi

        index_bracket=`expr index "$line" }`
        if [[ $index_bracket != 0 ]]; then
                count_bracket=`expr $count_bracket - 1`
                if [[ $find_flag == true ]]; then
                        if [[ $count_bracket == 0 ]]; then
                                index=`expr $index + 1`
                                find_flag=false
                        fi
                fi
        fi

        start=`echo ${line:0:4}`
        if [[ $start == 'host' ]]; then
                #echo count_bracket = $count_bracket
                if [[ $count_bracket == 1 ]]; then
                        arr_host_name[$index]=`echo $line | awk '{ print $2 }'`
                        find_flag=true
                fi
        fi
done < $1

for (( item=0; item<$index; ++item ))
do
        printf "%s\n" ${arr_host_name[$item]}
        printf "%s\n" ${arr_host_mac[$item]}
        printf "%s\n" ${arr_host_ip[$item]}
done
