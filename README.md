<div align="center"><a name="readme-top"></a>
  
  <img width=150 alt="OAuth banner image" src="https://github.com/user-attachments/assets/03040ea2-0385-4d07-81df-6e4ea6ed3b7c">

# OAuth 2.0 para RSE
  
  ![GitHub Created At](https://img.shields.io/github/created-at/alerone/OAuthRSE%20?color=%234F1787)
  ![GitHub contributors](https://img.shields.io/github/contributors/alerone/OAuthRSE?COLOR=%23FF6500)
  ![GitHub top language](https://img.shields.io/github/languages/top/alerone/OAuthRSE?color=%231230AE)
  ![Last commit](https://img.shields.io/github/last-commit/alerone/OAuthRSE?color=%23005B41)
  ![GitHub repo size](https://img.shields.io/github/repo-size/alerone/OAuthRSE?color=%23704264)

Este es un proyecto para probar el OAuth 2.0 para autenticar y autorizar usuarios en una pequeña aplicación web de prueba para crear y gestionar una lista de tareas.

</div>

## Instalación

Para instalar el proyecto debes primero descargar el código fuente del repositorio.

```bash
  git clone https://github.com/alerone/OAuthRSE.git
```

A continuación, deberás crear los archivos de configuración `secrets.json` y `.env`. Para el .env, puedes seguir el archivo `.env.example` que se encuentra en la raíz del proyecto.

El archivo secrets.json es más complicado de generar pues hay que hacerlo siguiendo el tutorial de Google para crear un ID de OAuth en un proyecto: 

https://developers.google.com/identity/protocols/oauth2?hl=es-419

Debes indicar como ``redirect_uri'': http://localhost:5000/auth/callback. Al final, el archivo secrets.json debe tener una estructura como la siguiente:

```json
{
    "installed": {
        "client_id": "<client-id>.apps.googleusercontent.com",
        "project_id": "oauthrse",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": "<client-secret>",
        "redirect_uris": [
            "http://localhost:5000/auth/callback"
        ]
    }
}
```

> [!IMPORTANT]
> Deberás seleccionar alguna cuenta de Google para probar la aplicación web pues al ser 
> solo de prueba, Google no puede comprobar que no se está utilizando de forma peligrosa
> la información de los usuarios que acceden a ella y sólo servirá para las cuentas de 
> Gmail que estén seleccionadas para probar el servicio.

Debes tener instalado docker en la máquina para seguir con la prueba y uso del servicio.
## Uso/Ejemplos

En la raíz del proyecto, abriendo un terminal, para probar el sistema tras haber realizado los pasos de instalación, deberás escribir la siguiente línea:

```bash
docker-compose up --build
```

Tras iniciar el sistema, se podrá acceder a este desde la ruta: http://localhost:5000
