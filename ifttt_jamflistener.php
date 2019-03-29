<?php
ini_set("error_log", "error.log");
error_reporting(E_ALL);

class IFTTT
{
	protected $key = null;
	protected $headers = array();
	protected $input = null;
	protected $params = array();
	protected $sample = array();
	protected $ts = null;
	
	public function __construct($key)
	{
		$this->key = $key;
		$this->headers = apache_request_headers();
		$this->input = json_decode(file_get_contents('php://input'));
		$this->ts = time();
		
		foreach ($_GET as $key => $value)
		{
			$this->params[$key] = $value;
		}
		
		array_push($this->sample, $this->createSample(123));
		array_push($this->sample, $this->createSample(124));
		array_push($this->sample, $this->createSample(125));
		
		$this->log('=====');
		$this->log('started');
		$this->log('key');
		$this->log($this->key);
		$this->log('params');
		$this->log(print_r($this->params, true));
		$this->log('request headers');
		$this->log(print_r($this->headers, true));
		$this->log('post body');
		$this->log(print_r($this->input, true));
		
		$this->authorize();
	}
	
	protected function authorize()
	{
		if ($this->headers['User-Agent'] === 'IFTTT-Protocol/v1')
		{
			if (!isset($this->headers['Ifttt-Channel-Key']) || ($this->headers['Ifttt-Channel-Key'] !== $this->key))
			{
				$this->log('auth failed');

				header("HTTP/1.1 401 Unauthorized");

				$this->respond(array(
					'errors'	=> array(
						array(
							'code'		=>	10001,
							'message'	=>	'Invalid channel/service key'
						)
					)
				));
			}
		}
		
		$this->log('auth successful');
	}

	public function trigger()
	{
		$this->log('running trigger');
		
		if (isset($this->input->limit))
		{
			if ($this->input->limit === 0) $this->respond(array('data' => array()));
			if ($this->input->limit === 1) $this->respond(array('data' => array($this->sample[0])));
		}
		else
		{
			if (file_exists('storage.json'))
			{
				$data = json_decode(file_get_contents('storage.json'));
				@unlink('storage.json');

				array_unshift($this->sample, array(
					'computer'					=>	$data->event->computer,
					'group_added_devices_ids'	=>	$data->event->groupAddedDevicesIds,
					'group_removed_devices_ids'	=>	$data->event->groupRemovedDevicesIds,
					'jssid'						=>	$data->event->jssid,
					'smart_group'				=>	$data->event->smartGroup,
					'name'						=>	$data->event->name,
					'created_at'				=>	date('c', time()),
					'meta'						=>	array(
						'id'					=>	bin2hex(openssl_random_pseudo_bytes(16)),
						'timestamp'				=>	time()
					)
				));
			}

			$this->respond(array('data' => $this->sample));
		}
	}
	
	public function action()
	{		
		$this->log('running action');
		
		//mail('MYEMAILADDRESS@krypted.com', 'ifttt', 'trigger fired, action done');
		
		// do something meaningful
		
		$this->respond(
			array(
				'data' => array(
					array('id' => bin2hex(openssl_random_pseudo_bytes(8)))
				)
			)
		);
	}
	
	public function status()
	{		
		$this->log('running status');
		
		$this->respond(
			array(
				'data' => array(
					'accessToken' => bin2hex(openssl_random_pseudo_bytes(16))
				)
			)
		);
	}
	
	protected function respond($out)
	{
		header('Content-type: application/json; charset=utf-8');
		echo json_encode($out);
		die();
	}
	
	protected function log($str)
	{
		$h = fopen('access.log', 'a+');
		fwrite($h, date('d-m-Y H:i:s') . " :: " . $str . "\r\n");
		fclose($h);
	}
	
	public function store()
	{
		$h = fopen('storage.json', 'w');
		fwrite($h, json_encode($this->input));
		fclose($h);
	}
	
	protected function createSample($id)
	{
		$this->ts = strtotime('21-01-2019');
		
		return array(
			'computer'					=>	'',
			'group_added_devices_ids'	=>	'',
			'group_removed_devices_ids'	=>	'',
			'jssid'						=>	'',
			'smart_group'				=>	'',
			'name'						=>	'sample name',
			'created_at'				=>	date('c', $this->ts),
			'meta'						=>	array(
				'id'					=>	$id,
				'timestamp'				=>	$this->ts
			)
		);
	}
}

// initialize the app with IFTTT service key
$app = new IFTTT('INSERTIFTTTSERVICEKEYHERE-uf');

switch ($_GET['act'])
{
	case 'status':
	case 'setup':
		$app->status();
		break;
	
	case 'store':
		$app->store();
		break;

	case 'trigger':
		$app->trigger();
		break;

	case 'action':
		$app->action();			
		break;			
}
