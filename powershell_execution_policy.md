# PowerShell Execution Policy Options

There are several ways to handle PowerShell script execution restrictions:

## Option 1: Temporarily bypass the execution policy

You can run the script by bypassing the execution policy for a single command:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_windows_tests.ps1
```

Or modify the run_tests.py file to use this approach:

```python
subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", ".\\run_windows_tests.ps1"], check=True)
```

## Option 2: Change the execution policy

You can change the execution policy for your user account (requires admin privileges):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

This allows you to run locally created scripts without signing, but requires downloaded scripts to be signed.

## Option 3: Sign the script

To sign a PowerShell script, you need a code signing certificate. Options include:

1. **Create a self-signed certificate** (for personal/development use):
   ```powershell
   New-SelfSignedCertificate -Subject "CN=PowerShell Code Signing" -Type CodeSigningCert -CertStoreLocation Cert:\CurrentUser\My
   ```

2. **Purchase a code signing certificate** from a Certificate Authority (CA) like:
   - DigiCert
   - Sectigo
   - GlobalSign
   - Comodo

3. **Use your organization's certificate** if you're part of a company that has a code signing infrastructure.

After obtaining a certificate, you can sign the script:

```powershell
# Get the certificate
$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert

# Sign the script
Set-AuthenticodeSignature -FilePath .\run_windows_tests.ps1 -Certificate $cert
```

## Option 4: Modify the script to run without PowerShell

You could rewrite the run_windows_tests.ps1 script as a Python script to avoid PowerShell execution policy issues altogether.

## Recommendation

For development purposes, Option 1 (bypassing the execution policy) or Option 2 (changing the execution policy to RemoteSigned) are the simplest approaches.

For production or distribution, Option 3 (signing the script) is more appropriate, but requires obtaining a certificate.
