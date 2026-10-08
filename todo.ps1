<#
.SYNOPSIS
    A simple command-line todo list manager.
.DESCRIPTION
    Usage:
        todo.ps1 add <text>    Add a task
        todo.ps1 list          Show tasks
        todo.ps1 done <n>      Mark or unmark task n
        todo.ps1 undo <n>      Same as done <n>
        todo.ps1 del <n>       Delete task n
        todo.ps1 help          Show help
#>

$ScriptDir = $PSScriptRoot
$DataFile = Join-Path $ScriptDir "todo.json"

function Load-Data {
    if (Test-Path $DataFile) {
        try {
            $data = Get-Content $DataFile -Raw | ConvertFrom-Json
            if ($data -is [Array]) {
                return $data
            }
            return @($data)
        } catch {
            Write-Warning "Failed to read data. Starting a fresh list."
            return @()
        }
    }
    return @()
}

function Save-Data {
    param([array]$items)
    $Json = $items | ConvertTo-Json -Depth 3
    $Json | Out-File -FilePath $DataFile -Encoding UTF8
}

function Show-Help {
    Write-Host "Todo CLI - Command-line todo list" -ForegroundColor Cyan
    Write-Host "Usage:"
    Write-Host "  todo.ps1 add <text>    Add a task"
    Write-Host "  todo.ps1 list          Show tasks"
    Write-Host "  todo.ps1 done <n>      Mark or unmark task n"
    Write-Host "  todo.ps1 undo <n>      Same as done <n>"
    Write-Host "  todo.ps1 del <n>       Delete task n"
    Write-Host "  todo.ps1 help          Show help"
}

function Show-List {
    [array]$items = Load-Data
    if ($items.Count -eq 0) {
        Write-Host "No todo items." -ForegroundColor Yellow
        return
    }
    Write-Host ("Todo list (" + $items.Count + " items):") -ForegroundColor Cyan
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $prefix = if ($item.IsDone) { "[x]" } else { "[ ]" }
        Write-Host ("{0,3}  {1}  {2}" -f $i, $prefix, $item.Content)
    }
    Write-Host ""
}

function Add-Item {
    param([string]$Content)
    if ([string]::IsNullOrWhiteSpace($Content)) {
        Write-Host "Task content cannot be empty." -ForegroundColor Red
        return
    }
    [array]$items = Load-Data
    $items += @{
        Content = $Content
        IsDone  = $false
        Id      = [guid]::NewGuid().ToString("N").Substring(0, 8)
    }
    Save-Data $items
    Write-Host ("Added: " + $Content) -ForegroundColor Green
}

function Set-ItemDone {
    param([int]$Index)
    [array]$items = Load-Data
    if ($Index -lt 0 -or $Index -ge $items.Count) {
        Write-Host ("Index out of range. Enter 0 to " + ($items.Count - 1) + ".") -ForegroundColor Red
        return
    }
    $items[$Index].IsDone = -not $items[$Index].IsDone
    Save-Data $items
    $status = if ($items[$Index].IsDone) { "done" } else { "not done" }
    Write-Host ("Index " + $Index + " is now " + $status) -ForegroundColor Green
}

function Remove-Item {
    param([int]$Index)
    [array]$items = Load-Data
    if ($Index -lt 0 -or $Index -ge $items.Count) {
        Write-Host ("Index out of range. Enter 0 to " + ($items.Count - 1) + ".") -ForegroundColor Red
        return
    }
    $content = $items[$Index].Content
    $items = $items | Where-Object { $_.Id -ne $items[$Index].Id }
    Save-Data $items
    Write-Host ("Deleted: " + $content) -ForegroundColor Red
}

$Command = $args[0]
switch ($Command) {
    "add" {
        if ($args.Count -lt 2) {
            Write-Host "Please provide task text." -ForegroundColor Red
            Show-Help
            return
        }
        Add-Item -Content ($args[1..($args.Count - 1)] -join " ")
    }
    "list" {
        Show-List
    }
    "done" {
        if ($args.Count -lt 2) {
            Write-Host "Please provide an index." -ForegroundColor Red
            Show-Help
            return
        }
        Set-ItemDone -Index ($args[1] - 1)
    }
    "undo" {
        if ($args.Count -lt 2) {
            Write-Host "Please provide an index." -ForegroundColor Red
            Show-Help
            return
        }
        Set-ItemDone -Index ($args[1] - 1)
    }
    "del" {
        if ($args.Count -lt 2) {
            Write-Host "Please provide an index." -ForegroundColor Red
            Show-Help
            return
        }
        Remove-Item -Index ($args[1] - 1)
    }
    "help" {
        Show-Help
    }
    default {
        Write-Host ("Unknown command: " + $Command) -ForegroundColor Red
        Show-Help
    }
}
