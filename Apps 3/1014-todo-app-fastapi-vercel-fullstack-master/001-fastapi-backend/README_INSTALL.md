# 🚀 Instalación de Dependencias - FastAPI Backend

Este directorio contiene scripts para instalar automáticamente todas las dependencias del proyecto FastAPI.

## 📋 Requisitos Previos

- **Python 3.8 o superior** instalado
- **pip** (gestor de paquetes de Python)
- **Conexión a internet** para descargar las librerías

## 🛠️ Opciones de Instalación

### Opción 1: Script Python (Recomendado)

```bash
# Navega al directorio del backend
cd 001-fastapi-backend

# Ejecuta el script de Python
python install_dependencies.py
```

**Características:**
- ✅ Interfaz interactiva
- ✅ Manejo de errores detallado
- ✅ Progreso visual
- ✅ Dos modos de instalación

### Opción 2: Script Batch (Windows)

```cmd
# Navega al directorio del backend
cd 001-fastapi-backend

# Ejecuta el script batch
install_dependencies.bat
```

**Características:**
- ✅ Automático (no requiere interacción)
- ✅ Verificaciones de sistema
- ✅ Mensajes de error claros

### Opción 3: Script PowerShell (Windows)

```powershell
# Navega al directorio del backend
cd 001-fastapi-backend

# Ejecuta el script de PowerShell
.\install_dependencies.ps1
```

**Características:**
- ✅ Colores en la terminal
- ✅ Verificaciones detalladas
- ✅ Manejo de errores robusto

### Opción 4: Instalación Manual

```bash
# Navega al directorio del backend
cd 001-fastapi-backend

# Actualiza pip
python -m pip install --upgrade pip

# Instala todas las dependencias
pip install -r requirements.txt
```

## 📦 Dependencias Principales

El archivo `requirements.txt` incluye **186 librerías**, entre ellas:

### **Core del Backend:**
- `fastapi==0.104.1` - Framework web
- `uvicorn==0.24.0.post1` - Servidor ASGI
- `sqlalchemy==2.0.23` - ORM para base de datos
- `psycopg2==2.9.9` - Driver de PostgreSQL
- `pydantic==2.5.2` - Validación de datos
- `alembic` - Migraciones de base de datos

### **Configuración:**
- `python-dotenv==1.0.0` - Variables de entorno
- `pydantic-settings==2.1.0` - Configuración tipada

### **Utilidades:**
- `requests==2.31.0` - Cliente HTTP
- `python-json-logger==2.0.7` - Logging estructurado

## 🔧 Solución de Problemas

### **Error: "Python no está instalado"**
```bash
# Descarga Python desde:
# https://python.org/downloads/
```

### **Error: "pip no está disponible"**
```bash
# Actualiza pip
python -m pip install --upgrade pip
```

### **Error: "No se encontró requirements.txt"**
```bash
# Asegúrate de estar en el directorio correcto
cd 001-fastapi-backend
ls requirements.txt  # Debe existir
```

### **Error de permisos (Windows)**
```powershell
# Ejecuta PowerShell como administrador
# O habilita la ejecución de scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### **Error de dependencias conflictivas**
```bash
# Crea un entorno virtual
python -m venv venv

# Activa el entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instala las dependencias
pip install -r requirements.txt
```

## 🎯 Próximos Pasos

Después de instalar las dependencias:

1. **Configura las variables de entorno:**
   ```bash
   # Crea archivo .env
   cp .env.example .env
   # Edita .env con tus credenciales de base de datos
   ```

2. **Ejecuta las migraciones:**
   ```bash
   alembic upgrade head
   ```

3. **Inicia el servidor:**
   ```bash
   uvicorn main:app --reload
   ```

4. **Verifica la instalación:**
   - Abre http://localhost:8000
   - Revisa la documentación en http://localhost:8000/docs

## 📊 Información del Proyecto

- **Total de dependencias:** 186 librerías
- **Tiempo estimado de instalación:** 5-10 minutos
- **Espacio requerido:** ~500MB
- **Versión de Python:** 3.8+

## 🤝 Contribución

Si encuentras problemas con la instalación:

1. Verifica que tienes Python 3.8+ instalado
2. Actualiza pip a la última versión
3. Intenta con un entorno virtual
4. Revisa los logs de error para más detalles

---

¡Listo para desarrollar! 🚀 