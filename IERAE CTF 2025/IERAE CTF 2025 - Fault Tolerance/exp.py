#!/usr/bin/env python3

import socket
import sys


def solve():
    # 读取当前的test111.js文件内容
    try:
        with open("test111.js", "r") as f:
            js_code = f.read().strip()
    except:
        # 如果文件不存在，使用备用代码
        js_code = """
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
"""
    
    return js_code


def connect_and_solve():
    host = "34.146.119.119"
    port = 9319

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))

        # Receive initial prompt
        data = s.recv(1024)
        print("Received:", data.decode())

        js_code = solve()

        # Send length
        length = str(len(js_code)) + '\n'
        s.send(length.encode())
        print(f"Sent length: {len(js_code)}")

        # Receive prog prompt
        data = s.recv(1024)
        print("Received:", data.decode())

        # Send the JavaScript code
        s.send(js_code.encode())
        print("Sent JavaScript code")

        # Receive response
        while True:
            try:
                data = s.recv(4096)
                if not data:
                    break
                print(data.decode(), end='')
            except:
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()


if __name__ == "__main__":
    if (len(sys.argv) > 1 and sys.argv[1] == "local") or len(sys.argv) == 1:
        # Test locally
        js_code = solve()
        print(f"Generated JavaScript code (length: {len(js_code)}):")
        print("=" * 50)
        print(js_code)
        print("=" * 50)
        print("\nTesting locally...")

        # Test removing each character
        failed_positions = []
        success_count = 0
        
        for i in range(len(js_code)):
            modified = js_code[:i] + js_code[i+1:]
            
            # Write to temp file and test
            with open("test_temp.js", "w") as f:
                f.write(modified)

            import subprocess
            try:
                result = subprocess.run(["node", "test_temp.js"], capture_output=True, text=True, timeout=5)
                
                # Check if it meets the requirements
                if result.returncode == 0 and "hello" in result.stdout:
                    print(f"✅ Position {i+1}/{len(js_code)} (char: {repr(js_code[i])}) - SUCCESS")
                    success_count += 1
                else:
                    print(f"❌ Position {i+1}/{len(js_code)} (char: {repr(js_code[i])}) - FAILED")
                    print(f"   Return code: {result.returncode}")
                    print(f"   Stdout: {repr(result.stdout)}")
                    print(f"   Stderr: {repr(result.stderr)}")
                    failed_positions.append(i)

            except Exception as e:
                print(f"❌ Position {i+1}/{len(js_code)} (char: {repr(js_code[i])}) - ERROR: {e}")
                failed_positions.append(i)

        print(f"\n\n=== SUMMARY ===")
        print(f"Total positions tested: {len(js_code)}")
        print(f"Successful tests: {success_count}")
        print(f"Failed positions: {len(failed_positions)}")
        print(f"Success rate: {success_count / len(js_code) * 100:.1f}%")
        
        if failed_positions:
            print(f"\nFirst 20 failed positions: {failed_positions[:20]}")
            print("Failed characters:")
            for pos in failed_positions[:10]:
                print(f"  Position {pos}: {repr(js_code[pos])}")
        
        if success_count == len(js_code):
            print("\n🎉 ALL TESTS PASSED! Ready for remote submission!")
        else:
            print(f"\n⚠️  {len(failed_positions)} tests failed. Need to improve the solution.")

    elif len(sys.argv) > 1 and sys.argv[1] == "remote":
        # Try connecting to remote server
        print("Attempting to connect to remote server...")
        connect_and_solve()
    else:
        print("Usage: python exp.py [local|remote]")
        print("  local  - Test the solution locally")
        print("  remote - Connect to remote server")
        print("  (no args) - Test locally")