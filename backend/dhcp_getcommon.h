#!/bin/bash

line_count=1
index_arr=0
arr_line_for_delete=()



function readConfig()
{
	local count_bracket=0
	local find_flag=false
	local index=0

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
}

writeConfig()
{
	count_bracket=0
	find_flag=false
	index=0

	arr_host_name=()
	arr_host_mac=()
	arr_host_ip=()


	while read line
	do
		index_bracket=`expr index "$line" {`
		if [[ $index_bracket != 0 ]]; then
			count_bracket=`expr $count_bracket + 1`
	    fi
	
		index_bracket=`expr index "$line" }`
	    if [[ $index_bracket != 0 ]]; then
	        count_bracket=`expr $count_bracket - 1`
			if [[ $find_flag == true ]]; then
				if [[ $count_bracket == 0 ]]; then
					sed -i ${line_count}d $1
					line_count=`expr $line_count - 1`
					arr_line_for_delete[$index_arr]=$line_count
					index_arr=`expr $index_arr + 1`
					find_flag=false
				fi
			fi
		fi
		
		if [[ $find_flag == true ]]; then
			arr_line_for_delete[$index_arr]=$line_count
			index_arr=`expr $index_arr + 1`
			sed -i ${line_count}d $1
			line_count=`expr $line_count - 1`
		fi
	
		start=`echo ${line:0:4}`
		if [[ $start == 'host' ]]; then
			if [[ $count_bracket == 1 ]]; then
				find_flag=true		
				arr_line_for_delete[$index_arr]=$line_count
				index_arr=`expr $index_arr + 1`
				sed -i ${line_count}d $1
				line_count=`expr $line_count - 1`
			fi
		fi
			
		line_count=`expr $line_count + 1`
				
	done < $1


	#for (( item=0; item<$index_arr; ++item ))
	#do
	#	printf "%s\n" ${arr_line_for_delete[$item]}
	#	sed -i ${arr_line_for_delete[$item]}d $1
	#	#printf "%s\n" ${arr_host_mac[$item]}
	#	#printf "%s\n" ${arr_host_ip[$item]}
	#done
	
	
	read -a arr1 <<< "${BASH_ARGV[@]}"
	for (( i=${#arr1[@]}-3; i>=0 ; i-=3 ))
	do 
		i2=`expr $i - 1`
		i3=`expr $i - 2`
		printf "host %s {\n   hardware ethernet %s\n   fixed-address %s\n}\n"  ${arr1[i]} ${arr1[i2]} ${arr1[i3]}>> $1
	done 
}


if [ $# -eq 1 ]; then
        echo "Error"
        exit 1
fi

if [[ $2 == "read" ]]; then
    readConfig $1
else
    writeConfig $1
fi
