# --*-- coding:utf-8 --*--
import subprocess
import zipfile
import os
import sys

#################################### 源文件目录 #################################
# 资源存储路径
resInputDir = "app/src/main/res"
# java 代码存储路径
javaInputDir = "app/src/main/java"
# Manifest文件
manifestFile = "app/src/main/AndroidManifest.xml"
# Android 源码
androidJarFile = "/Users/michael/Documents/Michael/Android/android-sdk-macosx/platforms/android-28/android.jar"

#################################### 生成文件存放目录 #################################
# build 文件夹
buildDir = "app/manual"
# 存放临时文件
tempDir = "app/manual/temp"
# 编译后的资源文件
resOutputDir = "app/manual/res"
# 生成的 R 文件
rOutputDir = "app/manual/r"
# 编译后的 class 文件
classesOutputDir = "app/manual/classes"
# 编译后的 dex 文件
dexOutputDir = "app/manual/dex"
# 生成的 apk 文件
apkOutputDir = "app/manual/apk"


def aapt2_compile():
    zipRes = "{dir}/compile.zip".format(dir=tempDir)
    subprocess.call(["aapt2", "compile", "--pseudo-localize", "-o", zipRes, "--dir", resInputDir])
    zipfile.ZipFile(zipRes, 'r').extractall(resOutputDir)


def aapt2_link():
    seperator = " {resOutputDir}/".format(resOutputDir=resOutputDir)
    filesStr = resOutputDir + "/" + seperator.join(os.listdir(resOutputDir))
    cmd = "aapt2 link -o {apkOutputDir}/res.apk -I {androidJarFile} --manifest {manifestFile} --java {rOutputDir} --target-sdk-version 26 {filesStr}".format(
        apkOutputDir=apkOutputDir, androidJarFile=androidJarFile, manifestFile=manifestFile, rOutputDir=rOutputDir, filesStr=filesStr)
    subprocess.call(cmd, shell=True)


def javac():
    rFile = rOutputDir + "/com/michael/test/R.java"
    javaFile = javaInputDir + "/com/michael/test/MainActivity.java"
    cmd = "javac -bootclasspath {androidJarFile} -d {classesOutputDir} {rFile} {javaFile}".format(
        androidJarFile=androidJarFile, classesOutputDir=classesOutputDir, rFile=rFile, javaFile=javaFile)
    subprocess.call(cmd, shell=True)


def d8():
    cmd = "d8 {classesOutputDir}/com/michael/test/*.class --lib {androidJarFile} --output {dexOutputDir}".format(
        classesOutputDir=classesOutputDir, androidJarFile=androidJarFile, dexOutputDir=dexOutputDir)
    subprocess.call(cmd, shell=True)


def apkbuilder():
    cmd = "apkbuilder {apkOutputDir}/unsign_unalign_app.apk -v -u -z {apkOutputDir}/res.apk -f {dexOutputDir}/classes.dex".format(
        apkOutputDir=apkOutputDir, dexOutputDir=dexOutputDir)
    subprocess.call(cmd, shell=True)


def zipalign():
    cmd = "zipalign 4 {apkOutputDir}/unsign_unalign_app.apk {apkOutputDir}/unsign_aligned_app.apk".format(
        apkOutputDir=apkOutputDir)
    subprocess.call(cmd, shell=True)


def apksigner():
    cmd = "apksigner sign --ks ~/.android/debug.keystore --ks-key-alias androiddebugkey --ks-pass pass:android --key-pass pass:android --out {apkOutputDir}/signed_aligned_app.apk {apkOutputDir}/unsign_aligned_app.apk".format(
        apkOutputDir=apkOutputDir)
    subprocess.call(cmd, shell=True)


def clean():
    for f in os.listdir(tempDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(tempDir, f)), shell=True)

    for f in os.listdir(resOutputDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(resOutputDir, f)), shell=True)

    for f in os.listdir(dexOutputDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(dexOutputDir, f)), shell=True)

    for f in os.listdir(rOutputDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(rOutputDir, f)), shell=True)

    for f in os.listdir(apkOutputDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(apkOutputDir, f)), shell=True)

    for f in os.listdir(classesOutputDir):
        subprocess.call(
            "rm -rf {dir}".format(dir=os.path.join(classesOutputDir, f)), shell=True)


def build():
    aapt2_compile()
    aapt2_link()
    javac()
    d8()
    apkbuilder()
    zipalign()
    apksigner()


if __name__ == '__main__':
    arg = sys.argv[1]
    if arg == "build":
        build()
    if arg == "clean":
        clean()
    if arg == "aapt2_compile":
        aapt2_compile()
    if arg == "aapt2_link":
        aapt2_link()
    if arg == "javac":
        javac()
    if arg == "d8":
        d8()
    if arg == "apkbuilder":
        apkbuilder()
    if arg == "zipalign":
        zipalign()
    if arg == "apksigner":
        apksigner()
