# IERAE CTF 2025 - Fault Tolerance

是一道关于**放射线耐性代码**（Radiation-hardened Code）的题。要求写个JavaScript，满足：

1. 删除程序中的任意一个字符后，能正常运行
2. 必须输出 `"hello\n"`
3. 长度不超过1500字符

这种类型的被称为"放射线耐性Quine"，灵感来源于航天领域 - 太空中的宇宙射线可能会翻转内存中的位，导致程序出错，因此需要设计能够容错的代码。

## 源码

```python
#!/usr/bin/env python3

"""

Your task is to write a JavaScript code that works even if any one character of it is removed.
Specifically, you must give to this script a string `prog` that meets the following conditions:

  * For any integer i (0 <= i < `len(prog)`), `prog[:i] + prog[i+1:]` is recognized as a valid JavaScript code and outputs `"hello\n"`.
  * `len(prog)` must be smaller than or equal to 1500.

Do not try to save something to files and reuse it, as it would fail.

"""

import sys
import string
import random
import tempfile
import subprocess

def myassert(cond, msg):
  if not cond:
    print(msg)
    sys.exit(1)

def main():
  sys.stdout.write('Input length: ')

  prog_len = int(sys.stdin.readline()[:-1])
  myassert(1 <= prog_len, "Don't hack!")
  myassert(prog_len <= 1500, "len(prog) must be smaller than or equal to 1500")

  sys.stdout.write('Input prog: ')

  prog = ''
  for i in range(prog_len):
    prog += sys.stdin.read(1)
  myassert(prog_len == len(prog), "EOF detected")

  verified = False

  # fault tolerance
  for i in range(prog_len):
    print('\n# i={}'.format(i))

    code = prog[:i] + prog[i+1:]

    with tempfile.NamedTemporaryFile(mode='w') as f:
      f.write(code)
      f.flush()

      # check if the program outputs "hello\n"

      subprocess.run(['chmod', 'o+r', f.name])
      result = subprocess.run(['sudo', '-u', 'nobody', 'node', f.name], capture_output=True)
      myassert(result.returncode == 0, "node should exit normally")

      output = result.stdout
      print('output: {}'.format(output))

      myassert(output == b'hello\n', 'the program should output "hello\\n"')
      verified = True

  myassert(verified, 'How did you fool it?')

  with open('./flag.txt') as f:
    flag = f.read()

  print('Well done!')
  print('The flag is {}'.format(flag))

if __name__ == '__main__':
  main()

```

## 思路

### 核心挑战

1. **字符串脆弱性**：直接使用 `console.log('hello')` 会在删除引号时出错
2. **语法完整性**：任何语法关键字的破坏都可能导致程序崩溃
3. **执行路径保证**：必须确保至少有一条执行路径能够成功

### 关键技术

#### 1. 多重变量赋值
```javascript
aaa=aa=unction=Fnction=Fuction=Funtion=Funcion=Functon=Functin=Functio=
Function
```

这一行创建了多个指向 `Function` 构造函数的变量：
- `unction` = 删除F后的Function
- `Fnction` = 删除u后的Function  
- `Fuction` = 删除n后的Function
- 以此类推...

无论删除 `Function` 中的哪个字母，都有对应的预定义变量可用。

#### 2. 安全的字符串输出
```javascript
String.fromCharCode(104,101,108,108,111)
```

使用字符编码而不是直接字符串：
- `104='h'`, `101='e'`, `108='l'`, `108='l'`, `111='o'`
- 删除数字位不会造成语法错误
- 确保输出的总是完整的 "hello"

#### 3. 保护性注释
```javascript
"(()=>{console.log(String.fromCharCode(104,101,108,108,111));process.exit(0)})()//"///"
```

使用 `//` 注释保护：
- 如果删除引号，代码会被注释掉而不报错
- 提供语法安全性

#### 4. 多重执行路径
```javascript
aaa.length==81&&Function`///${aaa}}```///`
aaa=
"(()=>{console.log(String.fromCharCode(104,101,108,108,111));process.exit(0)})()//"///"
Function`///${aaa}}```///`
```

提供多个执行点：
- 长度检查执行
- 重复赋值和执行
- 确保至少有一个路径成功

#### 5. 变量提升！
```javascript
var

ar,vr,va,aaalength,unction,Fnction,Fuction,Funtion,Funcion,Functon,Functin,Functio
var

ar,vr,va
```

利用JavaScript变量提升特性：
- 空行增加"缓冲字符"
- 重复声明提供备份
- 大部分删除不影响变量声明

## Payload

```javascript
aaa=aa=unction=Fnction=Fuction=Funtion=Funcion=Functon=Functin=Functio=
Function
aaa=aa=
"(()=>{console.log(String.fromCharCode(104,101,108,108,111));process.exit(0)})()//"///"
aaa.length==81&&Function`///${aaa}}```///`
aaa=
"(()=>{console.log(String.fromCharCode(104,101,108,108,111));process.exit(0)})()//"///"
Function`///${aaa}}```///`
var

ar,vr,va,aaalength,unction,Fnction,Fuction,Funtion,Funcion,Functon,Functin,Functio
var

ar,vr,va
```


