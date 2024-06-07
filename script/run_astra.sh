source ~/intel/oneapi/setvars.sh
echo 'run astra' $1 $2 $3
$1/.exe/astra  $2 $3 

case $4 in

  pause)
    echo -n "pause"
    read -p "Press enter to continue"
    ;;

  timeout)
    echo -n "timeout"
    secs=$((1 * 60))
    while [ $secs -gt 0 ]; do
    echo -ne "$secs\033[0K\r"
    sleep 1
    : $((secs--))
    done
    ;;

  no_pause)
    echo -n "no_pause"
    ;;

  *)
    echo -n "no_pause"
    ;;
esac




