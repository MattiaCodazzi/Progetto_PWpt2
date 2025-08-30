# ============================================
# Wizard GUI Setup - Progetto Museo (Windows)
# - Usa .venv se presente (altrimenti py/python)
# - Gestisce avvio da \scripts\
# - Installa requirements
# - PostgreSQL (utente, db) + import dump facoltativo
# - Avvio runserver
# ============================================

$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

function Log {
    param([string]$msg, [string]$color = "Black")
    $tbLog.SelectionColor = [System.Drawing.Color]::$color
    $tbLog.AppendText("[$((Get-Date).ToString('HH:mm:ss'))] $msg`r`n")
    $tbLog.ScrollToCaret()
    [System.Windows.Forms.Application]::DoEvents()
}
function SetStep {
    param([int]$i, [int]$tot, [string]$status)
    $progress.Value = [Math]::Min([int](($i / [double]$tot) * 100),100)
    $lblStatus.Text = $status
    [System.Windows.Forms.Application]::DoEvents()
}

function Get-SystemPy {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($py) { return $py.Source }
    $py2 = Get-Command python -ErrorAction SilentlyContinue
    if ($py2) { return $py2.Source }
    return $null
}

# ----------------- UI -----------------
$form = New-Object System.Windows.Forms.Form
$form.Text = "Installazione Progetto Museo"
$form.StartPosition = "CenterScreen"
$form.Size = New-Object System.Drawing.Size(950, 700)
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false

$lblTitle = New-Object System.Windows.Forms.Label
$lblTitle.Text = "Installazione Progetto (Django + PostgreSQL)"
$lblTitle.Font = New-Object System.Drawing.Font("Segoe UI",12,[System.Drawing.FontStyle]::Bold)
$lblTitle.AutoSize = $true
$lblTitle.Location = New-Object System.Drawing.Point(16,16)

[int]$y0 = 60
function LBL([string]$text,[int]$x,[int]$y){ $l=New-Object System.Windows.Forms.Label; $l.Text=$text; $l.AutoSize=$true; $l.Location=New-Object System.Drawing.Point($x,$y); $l }
function TB([int]$w,[int]$x,[int]$y){ $t=New-Object System.Windows.Forms.TextBox; $t.Width=$w; $t.Location=New-Object System.Drawing.Point($x,$y); $t }

$form.Controls.Add($lblTitle)

$form.Controls.Add((LBL "Cartella progetto (dove c'è manage.py):" 16 $y0))
$tbProject = TB 560 200 $y0; $tbProject.Text = (Split-Path (Get-Location).Path -Parent)

$btnBrowse = New-Object System.Windows.Forms.Button
$btnBrowse.Text="Sfoglia"
$btnBrowse.Location=New-Object System.Drawing.Point(770, ($y0 - 2))
$btnBrowse.Width=40

# --- DB ---
$form.Controls.Add((LBL "DB Name:" 16 ($y0 + 38)))
$tbDbName = TB 180 200 ($y0 + 35); $tbDbName.Text = "museo_db"

$form.Controls.Add((LBL "DB User:" 400 ($y0 + 38)))
$tbDbUser = TB 160 480 ($y0 + 35); $tbDbUser.Text = "museo_user"

$form.Controls.Add((LBL "DB Pass:" 16 ($y0 + 72)))
$tbDbPass = TB 180 200 ($y0 + 69); $tbDbPass.Text = "museo_pw"; $tbDbPass.UseSystemPasswordChar = $true

$form.Controls.Add((LBL "Dump .sql (facoltativo):" 400 ($y0 + 72)))
$tbDump = TB 260 560 ($y0 + 69); $tbDump.Text = ""
$btnBrowseDump = New-Object System.Windows.Forms.Button
$btnBrowseDump.Text="..."
$btnBrowseDump.Location=New-Object System.Drawing.Point(830, ($y0 + 67))
$btnBrowseDump.Width=20

# --- SUPERUSER ---
$form.Controls.Add((LBL "Superuser:" 16 ($y0 + 110)))
$tbSU = TB 180 200 ($y0 + 107); $tbSU.Text = "admin"

$form.Controls.Add((LBL "Email:" 400 ($y0 + 110)))
$tbEmail = TB 260 560 ($y0 + 107); $tbEmail.Text = "admin@example.com"

$form.Controls.Add((LBL "Password:" 16 ($y0 + 144)))
$tbSUPass = TB 180 200 ($y0 + 141); $tbSUPass.Text = "admin123"; $tbSUPass.UseSystemPasswordChar = $true

$chkRun = New-Object System.Windows.Forms.CheckBox
$chkRun.Text = "Avvia server Django a fine installazione"
$chkRun.Location = New-Object System.Drawing.Point(16, ($y0 + 176))
$chkRun.Width = 360
$chkRun.Checked = $true

$progress = New-Object System.Windows.Forms.ProgressBar
$progress.Location = New-Object System.Drawing.Point(16, ($y0 + 206))
$progress.Size = New-Object System.Drawing.Size(790, 20)

$lblStatus = New-Object System.Windows.Forms.Label
$lblStatus.Text = "Pronto"
$lblStatus.AutoSize = $true
$lblStatus.Location = New-Object System.Drawing.Point(16, ($y0 + 231))

# Link cliccabile per aprire il sito (inizialmente nascosto)
$lnkSite = New-Object System.Windows.Forms.LinkLabel
$lnkSite.Text = "Apri il sito → http://127.0.0.1:8000"
$lnkSite.AutoSize = $true
$lnkSite.Font = New-Object System.Drawing.Font("Segoe UI", 10, [System.Drawing.FontStyle]::Bold)
$lnkSite.LinkColor = [System.Drawing.Color]::Blue
$lnkSite.Location = New-Object System.Drawing.Point(16, ($y0 + 232))  # proprio sopra al log
$lnkSite.Visible = $false
$lnkSite.Add_Click({ Start-Process $lnkSite.Text.Split("→")[-1].Trim() })
$form.Controls.Add($lnkSite)


$tbLog = New-Object System.Windows.Forms.RichTextBox
$tbLog.Location = New-Object System.Drawing.Point(16, ($y0 + 256))
$tbLog.Size = New-Object System.Drawing.Size(790, 360)
$tbLog.ReadOnly = $true
$tbLog.BackColor = [System.Drawing.Color]::White

$btnStart = New-Object System.Windows.Forms.Button
$btnStart.Text="Avvia"
$btnStart.Location=New-Object System.Drawing.Point(730,16)
$btnStart.Width=66
$btnStart.Height=28

$form.Controls.AddRange(@(
  $tbProject,$btnBrowse,
  $tbDbName,$tbDbUser,$tbDbPass,$tbDump,$btnBrowseDump,
  $tbSU,$tbEmail,$tbSUPass,$chkRun,$progress,$lblStatus,$tbLog,$btnStart
))

$btnBrowse.Add_Click({
    $fd = New-Object System.Windows.Forms.FolderBrowserDialog
    if($fd.ShowDialog() -eq "OK"){ $tbProject.Text = $fd.SelectedPath }
})
$btnBrowseDump.Add_Click({
    $od = New-Object System.Windows.Forms.OpenFileDialog
    $od.Filter = "SQL Dump|*.sql|Tutti i file|*.*"
    if($od.ShowDialog() -eq "OK"){ $tbDump.Text = $od.FileName }
})

# ----------------- helpers -----------------
function Exec {
    param([string]$cmd, [switch]$Quiet)
    Log "RUN> $cmd" "Gray"
    $pinfo = New-Object System.Diagnostics.ProcessStartInfo
    $pinfo.FileName = "powershell"
    $pinfo.Arguments = "-NoProfile -Command `$ErrorActionPreference='Stop'; $cmd"
    $pinfo.RedirectStandardOutput = $true
    $pinfo.RedirectStandardError  = $true
    $pinfo.UseShellExecute = $false
    $pinfo.CreateNoWindow = $true
    # <<< FIX: mantieni la working dir corrente così .\requirements.txt funziona >>>
    $pinfo.WorkingDirectory = (Get-Location).Path
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo = $pinfo
    $null = $p.Start()
    $output = $p.StandardOutput.ReadToEnd()
    $err = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    if(-not $Quiet){ $output | ForEach-Object { Log "$_" } }
    if($err){ $err.Trim().Split("`n") | ForEach-Object { Log $_ "Red" } }
    if($p.ExitCode -ne 0){ throw "Comando fallito ($($p.ExitCode))" }
}

function ExecNative {
    param([string]$file, [string[]]$arguments)
    Log ("RUN> " + $file + " " + ($arguments -join " ")) "Gray"
    $p = New-Object System.Diagnostics.Process
    $p.StartInfo.FileName  = $file
    $p.StartInfo.Arguments = ($arguments -join " ")
    $p.StartInfo.RedirectStandardOutput = $true
    $p.StartInfo.RedirectStandardError  = $true
    $p.StartInfo.UseShellExecute = $false
    $p.StartInfo.CreateNoWindow = $true
    $p.StartInfo.WorkingDirectory = (Get-Location).Path
    $null = $p.Start()
    $stdOut = $p.StandardOutput.ReadToEnd()
    $stdErr = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    if($stdOut){ $stdOut.Trim().Split("`n") | ForEach-Object { Log $_ } }
    if($stdErr){ $stdErr.Trim().Split("`n") | ForEach-Object { Log $_ "Red" } }
    if($p.ExitCode -ne 0){ throw "Processo fallito ($($p.ExitCode)): $file" }
}

# ----------------- Core setup -----------------
function Invoke-Setup {
    param(
        [string]$ProjectPath,
        [string]$DbName, [string]$DbUser, [string]$DbPass, [string]$DumpPath,
        [string]$SuperUser, [string]$SuperEmail, [string]$SuperPass,
        [bool]$RunServer = $true
    )
    try{
        $btnStart.Enabled = $false
        $total = 10; $step = 1

        SetStep ($step++) $total "Controlli preliminari"
        if(-not (Test-Path $ProjectPath)){ throw "Cartella progetto non trovata: $ProjectPath" }
        Set-Location $ProjectPath

        # Se l'utente seleziona 'scripts', risalgo alla root (dove c'è manage.py)
        if (-not (Test-Path ".\manage.py") -and (Test-Path ".\scripts")) {
            Set-Location ..
            Log "Rilevato 'scripts': risalgo alla root $((Get-Location).Path)" "Gray"
        }
        if (-not (Test-Path ".\manage.py")) { throw "manage.py non trovato nella cartella: $((Get-Location).Path)" }

        # Scegli eseguibile Python: priorità al venv locale
        $script:PYEXE = $null
        $venvPy = Join-Path (Get-Location) ".venv\Scripts\python.exe"
        if (Test-Path $venvPy) {
            $script:PYEXE = $venvPy
            Log "Uso Python del venv: $PYEXE" "Gray"
        } else {
            $sysPy = Get-SystemPy
            if (-not $sysPy) { throw "Python non trovato. Installa Python 3 o crea il venv (.venv)." }
            $script:PYEXE = $sysPy
            Log "Uso Python di sistema: $PYEXE" "Yellow"
        }

        # ---- PostgreSQL: crea utente/db se necessario ----
        SetStep ($step++) $total "Configuro PostgreSQL (se necessario)"
        $psql = Get-Command psql -ErrorAction SilentlyContinue
        if ($psql) {
            $existsUser = & psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$DbUser';"
            if($existsUser.Trim() -ne "1"){
                ExecNative "psql" @("-U","postgres","-c","CREATE USER $DbUser WITH PASSWORD '$DbPass';")
                ExecNative "psql" @("-U","postgres","-c","ALTER USER $DbUser CREATEDB;")
                Log "Utente $DbUser creato" "Green"
            } else { Log "Utente $DbUser già esiste" "Cyan" }

            $existsDb = & psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$DbName';"
            if($existsDb.Trim() -ne "1"){
                ExecNative "psql" @("-U","postgres","-c","CREATE DATABASE $DbName OWNER $DbUser;")
                Log "Database $DbName creato" "Green"
            } else { Log "Database $DbName già esiste" "Cyan" }

            if($DumpPath -and (Test-Path $DumpPath)){
                SetStep ($step++) $total "Import dump SQL"
                ExecNative "psql" @("-U",$DbUser,"-d",$DbName,"-f",$DumpPath)
                Log "Dump importato: $DumpPath" "Green"
            }
        } else {
            Log "psql non trovato nel PATH: salto la sezione PostgreSQL" "Yellow"
        }

        # ---- Requirements ----
        SetStep ($step++) $total "Installo dipendenze"
        if (Test-Path ".\requirements.txt") {
            Exec "$env:ComSpec /c `"$PYEXE -m pip install --upgrade pip`""
            Exec "$env:ComSpec /c `"$PYEXE -m pip install -r .\requirements.txt`""
        } else {
            Exec "$env:ComSpec /c `"$PYEXE -m pip install django`""
        }

        # ---- Migrazioni ----
        SetStep ($step++) $total "Migrazioni Django"
        Exec "$env:ComSpec /c `"$PYEXE .\manage.py migrate`""
        Log "Migrate OK" "Green"

        # ---- Superuser ----
        SetStep ($step++) $total "Crea superuser Django (best effort)"
        $env:DJANGO_SUPERUSER_USERNAME = $SuperUser
        $env:DJANGO_SUPERUSER_EMAIL    = $SuperEmail
        $env:DJANGO_SUPERUSER_PASSWORD = $SuperPass
        try {
            Exec "$env:ComSpec /c `"$PYEXE .\manage.py createsuperuser --noinput`"" -Quiet
            Log "Superuser creato/già presente" "Green"
        } catch {
            Log "Creazione superuser: probabilmente già presente (OK)" "Yellow"
        }

        # ---- Collectstatic opzionale ----
        SetStep ($step++) $total "Collectstatic (opzionale)"
try {
    Exec "$env:ComSpec /c `"$PYEXE .\manage.py collectstatic --noinput`"" -Quiet
    Log "collectstatic completato" "Green"
} catch {
    Log "collectstatic saltato: $($_.Exception.Message)" "Yellow"
}


        if($RunServer){
    # URL locale visibile/correttamente cliccabile
    $serverUrl = "http://127.0.0.1:8000"

    SetStep ($step++) $total "Avvio server Django"
    # avvio server in una nuova PS, ma bind su 127.0.0.1 (così la console mostra l’URL giusto)
    Start-Process "powershell" "-NoExit -Command cd `"$([System.IO.Path]::GetFullPath($(Get-Location)))`"; & `"$PYEXE`" `".\manage.py`" runserver 127.0.0.1:8000"

    # evidenzio il link nel wizard e apro il browser
    $lnkSite.Text = "Apri il sito → $serverUrl"
    $lnkSite.Visible = $true
    Log "Sito avviato su $serverUrl" "Blue"
    Start-Process $serverUrl
}


        SetStep 100 100 "Completato"
        Log "Installazione completata!" "Green"
    }
    catch{
        Log "ERRORE: $($_.Exception.Message)" "Red"
    }
    finally{
        $btnStart.Enabled = $true
    }
}

$btnStart.Add_Click({
    Invoke-Setup -ProjectPath $tbProject.Text `
             -DbName $tbDbName.Text -DbUser $tbDbUser.Text -DbPass $tbDbPass.Text -DumpPath $tbDump.Text `
             -SuperUser $tbSU.Text -SuperEmail $tbEmail.Text -SuperPass $tbSUPass.Text `
             -RunServer $chkRun.Checked
})

$form.Add_Shown({ $form.Activate() })
[void]$form.ShowDialog()

