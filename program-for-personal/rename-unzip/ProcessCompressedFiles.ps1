# 自定义变量
$sourceDir = "D:\EnjoyLibrary\1000h-english-learning-record"          # 压缩文件所在目录
$destinationDir = "D:\EnjoyLibrary\1000h-english-learning-record" # 解压后的文件夹存放路径
$customPrefix = "xiaolai"                      # 日期前的自定义字符

# 扫描并处理压缩文件的函数
function Process-CompressedFiles {
    Get-ChildItem -Path $sourceDir -Filter "*.zip" | ForEach-Object {
        # 获取文件创建日期
        $creationDate = (Get-Item $_.FullName).CreationTime.ToString("yyyyMMdd")

        # 新的文件名
        $newFileName = "$customPrefix" + "_" + $creationDate + $_.Extension
        $newFilePath = Join-Path -Path $sourceDir -ChildPath $newFileName

        # 重命名文件
        Rename-Item -Path $_.FullName -NewName $newFilePath

        # 创建解压后的文件夹
        $extractedFolder = Join-Path -Path $destinationDir -ChildPath $newFileName.Replace($_.Extension, "")
        New-Item -Path $extractedFolder -ItemType Directory -Force

        # 解压文件
        Expand-Archive -Path $newFilePath -DestinationPath $extractedFolder -Force

        Write-Host "文件 '$newFileName' 解压至: $extractedFolder"
    }
}

# 设置定时任务，每隔10分钟执行一次
$trigger = New-JobTrigger -AtStartup -RepetitionInterval (New-TimeSpan -Minutes 10) -RepeatIndefinitely
Register-ScheduledJob -Name "ProcessCompressedFilesJob" -Trigger $trigger -FilePath "C:\path\to\script\ProcessCompressedFiles.ps1"
