param([string]$portName = "COM4", [int]$baud = 115200, [int]$durationMs = 4000)

$port = New-Object System.IO.Ports.SerialPort $portName, $baud
$port.DtrEnable = $true
$port.RtsEnable = $true
$port.ReadTimeout = 1000

try {
    $port.Open()
    Write-Output "=== SERIAL OPENED: $portName @ $baud ==="
    $sw = [System.Diagnostics.Stopwatch]::StartNew()
    while ($sw.ElapsedMilliseconds -lt $durationMs) {
        try {
            $line = $port.ReadLine()
            Write-Output $line
        } catch [System.TimeoutException] {
            # continue
        }
    }
} catch {
    Write-Error $_.Exception.Message
} finally {
    if ($port.IsOpen) {
        $port.Close()
        Write-Output "=== SERIAL CLOSED ==="
    }
}
