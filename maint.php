<?php
$nowtime = time();
#echo $nowtime;
$mins = date('i',$nowtime);
if ($mins %2 == 0 ) {
        echo "OK";
}
else {
        echo header("HTTP/1.1 503 Down for maintenance");
        echo "Down for maint";
}
?>