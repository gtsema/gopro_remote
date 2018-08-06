# -*- mode: python -*-

block_cipher = None


a = Analysis(['main.py'],
             pathex=['C:\\Users\Greg\\Documents\\Eclipse_projects\\gopro_remote'],
             binaries=[],
             datas=[('gopro_remote.ui', '.'), ('qwindows.dll', 'plugins\platforms'), ('qwindows.dll', 'platforms')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='GoPro 4 Hero remote',
          debug=False,
          strip=False,
          upx=True,
          console=False,
		  icon='gopro_64px.ico')
