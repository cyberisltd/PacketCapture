<html>
<body>
<form method="post" action="/cgi-bin/pcapdownload.cgi">
<table style="width: 100%">
				<tr>
								<td>PCAP Filter</td>
								<td><input name="bpffilter" type="text" size="50" value="<? print htmlspecialchars($_GET['bpffilter']);  ?>" /></td>
				</tr>
				<tr>
								<td>Start Time (YYYYMMDDHHMMSS)</td>
								<td><input name="starttime" type="text" size="50" value="<? print htmlspecialchars($_GET['starttime']);  ?>" /></td>
				</tr>
				<tr>
								<td>End Time (YYYYMMDDHHMMSS)</td>
								<td><input name="endtime" type="text" size="50" value="<? print htmlspecialchars($_GET['endtime']);  ?>" /></td>
				</tr>
				<tr>
								<td>Sensor name (i.e. bond0)</td>
								<td><input name="sensor" type="text" size="50" value="<? print htmlspecialchars($_GET['sensor']);  ?>" /></td>
				</tr>
				<tr>
								<td>&nbsp;</td>
								<td><input name="send" type="submit" value="Download" /></td>
				</tr>
</table>
</form>
</body>
</html>

