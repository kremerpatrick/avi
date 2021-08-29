<?php
$nowtime = time();
$hostname = gethostname();
echo $hostname . ' ';
$hostid = substr($hostname,-1);
#echo $hostid % 2;
$mins = date('i',$nowtime);
if ($mins %2 == $hostid ) {
        echo "OK";
}
else {
        echo header("HTTP/1.1 503 Down for maintenance");
        echo "Down for maint";
}
?>