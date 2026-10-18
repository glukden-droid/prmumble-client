# Prints how the PR launcher started PRMumble: exe path, command line, parent.
# Run on the game PC while connected to a server with mumble.
Get-CimInstance Win32_Process -Filter "Name='PRMumble.exe'" | ForEach-Object {
    $parent = Get-CimInstance Win32_Process -Filter "ProcessId=$($_.ParentProcessId)"
    [pscustomobject]@{
        Pid         = $_.ProcessId
        Path        = $_.ExecutablePath
        CommandLine = $_.CommandLine
        Parent      = "$($parent.Name) ($($_.ParentProcessId))"
        ParentCmd   = $parent.CommandLine
    } | Format-List
}
