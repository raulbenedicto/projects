import boto3
from datetime import timezone

session = boto3.Session(profile_name='cesarra')
s3_client = session.client('s3')

bucket_name = 'bkt-sor-storage-backup-rcb'
prefix = 'Backup_Camera_Tablet/'

# Listar objetos no bucket/prefixo
response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

# HTML inicial
html_content = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Lista de Arquivos S3</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; background-color: #f9f9f9; }
        table { width: 100%; border-collapse: collapse; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #4CAF50; color: white; }
        tr:hover { background-color: #f1f1f1; }
        a { color: #1a73e8; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
<h2>📂 Lista de Arquivos no Bucket S3</h2>
<table>
    <thead>
        <tr>
            <th>Arquivo</th>
            <th>Tamanho (KB)</th>
            <th>Última Modificação</th>
            <th>Tipo MIME</th>
            <th>Link</th>
        </tr>
    </thead>
    <tbody>
"""

if 'Contents' in response:
    for obj in response['Contents']:
        key = obj['Key']
        metadata = s3_client.head_object(Bucket=bucket_name, Key=key)

        # Gerar URL pré-assinada para cada objeto
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': key},
            ExpiresIn=3600
        )

        # Metadados
        file_name = key.split('/')[-1]
        file_size_kb = round(metadata['ContentLength'] / 1024, 2)
        last_modified = metadata['LastModified'].astimezone(timezone.utc).strftime("%d/%m/%Y %H:%M:%S UTC")
        mime_type = metadata.get('ContentType', 'N/A')

        # Inserindo linha na tabela HTML
        html_content += f"""
        <tr>
            <td>{file_name}</td>
            <td>{file_size_kb}</td>
            <td>{last_modified}</td>
            <td>{mime_type}</td>
            <td><a href="{url}" target="_blank">📥 Acessar</a></td>
        </tr>
        """
else:
    html_content += """
    <tr>
        <td colspan="5">Nenhum arquivo encontrado.</td>
    </tr>
    """

# Finalizando HTML
html_content += """
    </tbody>
</table>
</body>
</html>
"""

# Salvando arquivo HTML gerado
with open("lista_arquivos_metadados.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("✅ Página HTML com metadados gerada: lista_arquivos_metadados.html")