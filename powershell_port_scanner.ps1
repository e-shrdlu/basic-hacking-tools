$st = 7999
$en = 8001
$target = '10.2.45.162'
$WarningPreference='silentlycontinue'
for ($i=$st; $i -le $en; $i++){
    $conn = Test-NetConnection -ComputerName $target -Port $i
    $open = $conn | Where-Object -Property TcpTestSucceeded
    if ($open){
        echo "$i is open"
    }
}
