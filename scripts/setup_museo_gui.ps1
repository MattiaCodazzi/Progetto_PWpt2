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
# --- STILE GLOBALE (aggiungi subito dopo la creazione del $form)
$fontBase = New-Object System.Drawing.Font("Segoe UI", 10)
$form.Font      = $fontBase
$form.BackColor = [System.Drawing.Color]::WhiteSmoke
$form.AutoScaleMode = 'Dpi'

$form.Text = "Installazione Progetto Museo"
$form.StartPosition = "CenterScreen"
$form.Size = New-Object System.Drawing.Size(1100, 700)
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false

# --- TEMA GRAFICO (incolla dopo: $form = New-Object System.Windows.Forms.Form)
# Assicurati di avere già: Add-Type -AssemblyName System.Windows.Forms, System.Drawing

# Palette + font
$ui_FontName   = 'Segoe UI'
$ui_FontSize   = 10
$ui_FormBack   = [System.Drawing.Color]::WhiteSmoke
$ui_TextDark   = [System.Drawing.Color]::FromArgb(44,62,80)
$ui_PanelLight = [System.Drawing.Color]::Gainsboro
$ui_Primary    = [System.Drawing.Color]::FromArgb(41,128,185)  # blu
$ui_PrimaryHov = [System.Drawing.Color]::FromArgb(30,108,165)  # blu hover
$ui_Secondary  = [System.Drawing.Color]::FromArgb(236,240,241) # grigio chiaro
$ui_SecondaryH = [System.Drawing.Color]::FromArgb(220,224,225)

# Applica font/sfondo al form
$form.Font      = New-Object System.Drawing.Font($ui_FontName, $ui_FontSize)
$form.BackColor = $ui_FormBack


$lblTitle = New-Object System.Windows.Forms.Label
$lblTitle.Text = "Installazione Progetto (Django + PostgreSQL)"
$lblTitle.Font = New-Object System.Drawing.Font("Segoe UI",12,[System.Drawing.FontStyle]::Bold)
$lblTitle.AutoSize = $true
$lblTitle.Location = New-Object System.Drawing.Point(16,16)

[int]$y0 = 60
function LBL([string]$text,[int]$x,[int]$y){ $l=New-Object System.Windows.Forms.Label; $l.Text=$text; $l.AutoSize=$true; $l.Location=New-Object System.Drawing.Point($x,$y); $l }
function TB([int]$w,[int]$x,[int]$y){ $t=New-Object System.Windows.Forms.TextBox; $t.Width=$w; $t.Location=New-Object System.Drawing.Point($x,$y); $t }

$form.Controls.Add($lblTitle)

$form.Controls.Add((LBL "Cartella progetto (dove si trova manage.py):" 16 $y0))
$tbProject = TB 560 200 $y0; $tbProject.Text = (Split-Path (Get-Location).Path -Parent)

$btnBrowse = New-Object System.Windows.Forms.Button
$btnBrowse.Text = "Sfoglia"
$btnBrowse.AutoSize = $false
$btnBrowse.Width = 80
$btnBrowse.Height = 30
$btnBrowse.Location = New-Object System.Drawing.Point(770, ($y0 - 4))
# (opzionale, se usi le funzioni di stile)
# Set-SecondaryButtonStyle $btnBrowse


# --- DB ---
$form.Controls.Add((LBL "DB Name:" 16 ($y0 + 38)))
$tbDbName = TB 180 200 ($y0 + 35); $tbDbName.Text = "museo_db"

$form.Controls.Add((LBL "DB User:" 400 ($y0 + 38)))
$tbDbUser = TB 160 480 ($y0 + 35); $tbDbUser.Text = "museo_user"

$form.Controls.Add((LBL "DB Pass:" 16 ($y0 + 72)))
$tbDbPass = TB 180 200 ($y0 + 69); $tbDbPass.Text = "museo_pw"; $tbDbPass.UseSystemPasswordChar = $true

$form.Controls.Add((LBL "Dump .sql (facoltativo):" 400 ($y0 + 72)))
$tbDump = TB 260 560 ($y0 + 69)

# NUOVO CAMPO: Postgres admin pass (subito sotto DB Pass, a sinistra)
$form.Controls.Add((LBL "Postgres admin pass:" 16 ($y0 + 106)))
$tbPgAdminPass = TB 180 200 ($y0 + 103); $tbPgAdminPass.UseSystemPasswordChar = $true


# TextBox dump: più larga e in primo piano
$tbDump = TB 360 560 ($y0 + 69)
$tbDump.Text = ""
$tbDump.BackColor  = [System.Drawing.Color]::White
$tbDump.BorderStyle = 'FixedSingle'
$tbDump.BringToFront()

# Bottone "…" allineato alla textbox (niente coordinate fisse)
$btnBrowseDump = New-Object System.Windows.Forms.Button
$btnBrowseDump.Text      = "..."
$btnBrowseDump.AutoSize  = $false
$btnBrowseDump.Width     = 34     # 34–40 ok per "..."
$btnBrowseDump.Height    = 30
$btnBrowseDump.Location  = New-Object System.Drawing.Point(($tbDump.Right + 8), ($tbDump.Top - 1))




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
  $tbDbName,$tbDbUser,$tbDbPass,$tbDump,$btnBrowseDump,$tbPgAdminPass,
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




# --- FUNZIONI DI STILE (incolla prima di $form.ShowDialog())

function Set-PrimaryButtonStyle([System.Windows.Forms.Button]$btn) {
    $btn.FlatStyle = 'Flat'
    $btn.UseVisualStyleBackColor = $false
    $btn.BackColor = $ui_Primary
    $btn.ForeColor = [System.Drawing.Color]::White
    if ($btn.Height -lt 32) { $btn.Height = 32 }
    # hover
    $btn.Add_MouseEnter({ param($s,$e) $s.BackColor = $ui_PrimaryHov })
    $btn.Add_MouseLeave({ param($s,$e) $s.BackColor = $ui_Primary })
}

function Set-SecondaryButtonStyle([System.Windows.Forms.Button]$btn) {
    $btn.FlatStyle = 'Flat'
    $btn.UseVisualStyleBackColor = $false
    $btn.BackColor = $ui_Secondary
    $btn.ForeColor = $ui_TextDark
    if ($btn.Height -lt 30) { $btn.Height = 30 }
    # hover
    $btn.Add_MouseEnter({ param($s,$e) $s.BackColor = $ui_SecondaryH })
    $btn.Add_MouseLeave({ param($s,$e) $s.BackColor = $ui_Secondary })
}

function Style-AllControls([System.Windows.Forms.Control]$root) {
    foreach ($c in $root.Controls) {

        if ($c -is [System.Windows.Forms.Button]) {
            # prova a capire se è il "bottone principale" (Avvia/Start/Esegui)
            if ($c.Name -match 'btnStart|btnAvvia' -or $c.Text -match '^(Avvia|Start|Esegui)') {
                Set-PrimaryButtonStyle $c
            } else {
                Set-SecondaryButtonStyle $c
            }
        }
        elseif ($c -is [System.Windows.Forms.Label]) {
            $c.ForeColor = $ui_TextDark
        }
        elseif ($c -is [System.Windows.Forms.ProgressBar]) {
            # solo estetica, non tocca la logica
            try { $c.Style = 'Continuous' } catch {}
            if ($c.Height -lt 20) { $c.Height = 20 }
            # NB: il colore della progress bar spesso non è personalizzabile in WinForms classico
        }
        elseif ($c -is [System.Windows.Forms.Panel] -and $c.Dock -eq 'Bottom') {
            # se hai un pannello docked in basso (anche con nome diverso da $footer), rendilo più "footer"
            $c.BackColor = $ui_PanelLight
        }

        # ricorsione sui figli
        if ($c.Controls.Count -gt 0) {
            Style-AllControls $c
        }
    }
}

# Applica il tema all’intero form (non richiede $header/$footer esistenti)
Style-AllControls $form


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
        [string]$PgAdminPass, 
        [bool]$RunServer = $true

    )
    try{
        $btnStart.Enabled = $false
        $total = 10; $step = 1

        SetStep ($step++) $total "Controlli preliminari"

# Normalizza: rimuovi eventuali doppi apici e spazi ai bordi
if ($null -eq $ProjectPath) { $ProjectPath = "" }
$ProjectPath = $ProjectPath.Trim('"').Trim()


# Verifica percorso con -LiteralPath (gestisce spazi e caratteri speciali)
if (-not (Test-Path -LiteralPath $ProjectPath)) {
    throw "Cartella progetto non trovata: $ProjectPath"
}

# Vai nella cartella progetto (percorso risolto in forma canonica)
$projRoot = (Resolve-Path -LiteralPath $ProjectPath).Path
Set-Location -LiteralPath $projRoot

# Se l'utente ha selezionato la sottocartella 'scripts', risali alla root del progetto
if (-not (Test-Path -LiteralPath ".\manage.py") -and (Test-Path -LiteralPath ".\scripts")) {
    Set-Location -LiteralPath ..
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
            $env:PGPASSWORD = $PgAdminPass
            $existsUser = & psql -h 127.0.0.1 -U postgres -w -tAc "SELECT 1 FROM pg_roles WHERE rolname = '$DbUser';"
            Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

            if($existsUser.Trim() -ne "1"){
                $env:PGPASSWORD = $PgAdminPass
ExecNative "psql" @("-h","127.0.0.1","-U","postgres","-w","-c","CREATE USER $DbUser WITH PASSWORD '$DbPass';")
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

                $env:PGPASSWORD = $PgAdminPass
ExecNative "psql" @("-h","127.0.0.1","-U","postgres","-w","-c","ALTER USER $DbUser CREATEDB;")
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

                Log "Utente $DbUser creato" "Green"
            } else { Log "Utente $DbUser già esiste" "Cyan" }

            $env:PGPASSWORD = $PgAdminPass
$existsDb = & psql -h 127.0.0.1 -U postgres -w -tAc "SELECT 1 FROM pg_database WHERE datname = '$DbName';"
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

            if($existsDb.Trim() -ne "1"){
                $env:PGPASSWORD = $PgAdminPass
ExecNative "psql" @("-h","127.0.0.1","-U","postgres","-w","-c","CREATE DATABASE $DbName OWNER $DbUser;")
Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue

                Log "Database $DbName creato" "Green"
            } else { Log "Database $DbName già esiste" "Cyan" }

           if($DumpPath -and (Test-Path $DumpPath)){
    SetStep ($step++) $total "Import dump SQL"

    # 1) Se il DB ha tabelle nello schema public, lo resetto (DROP+CREATE) usando postgres
    $env:PGPASSWORD = $PgAdminPass
    try {
        $hasTables = & psql -h 127.0.0.1 -U postgres -w -d $DbName -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';"
        if ([int]$hasTables -gt 0) {
            Log "DB non vuoto: reset dello schema 'public' prima dell'import." "Yellow"
            & psql -h 127.0.0.1 -U postgres -w -d $DbName -v ON_ERROR_STOP=1 -c "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public AUTHORIZATION $DbUser; GRANT ALL ON SCHEMA public TO $DbUser; GRANT ALL ON SCHEMA public TO public;"
        }
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }

    # 2) Import del dump (password non interattiva per museo_user)
    $env:PGPASSWORD = $DbPass
    try {
        ExecNative "psql" @(
            "-h","127.0.0.1",
            "-U",$DbUser,
            "-d",$DbName,
            "-w",
            "-v","ON_ERROR_STOP=1",
            "-q",
            "-f","`"$DumpPath`""

        )
        Log "Dump importato: $DumpPath" "Green"
    }
    finally {
        Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
    }
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
    $projPath = "`"$([System.IO.Path]::GetFullPath($(Get-Location)))`""
    Start-Process "powershell" "-NoExit -Command cd $projPath; & `"$PYEXE`" `".\manage.py`" runserver 127.0.0.1:8000"


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
             -PgAdminPass $tbPgAdminPass.Text `
             -RunServer $chkRun.Checked
})

$form.Add_Shown({ $form.Activate() })
[void]$form.ShowDialog()

