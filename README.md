# Sistema de Gestión - Proyecto Semestral SI

Sistema de gestión profesional desarrollado con tecnologías web modernas. Interfaz intuitiva y responsive para la administración de usuarios, productos y reportes.

## 🚀 Características

- **Dashboard Interactivo**: Visualización de estadísticas y métricas clave
- **Gestión de Usuarios**: CRUD completo para administración de usuarios
- **Gestión de Productos**: Catálogo de productos con sistema de inventario
- **Diseño Responsive**: Adaptable a dispositivos móviles, tablets y escritorio
- **Modo Oscuro**: Alternancia entre tema claro y oscuro
- **Gráficos Dinámicos**: Visualización de datos con Chart.js
- **Interfaz Moderna**: Diseño profesional con gradientes y animaciones

## 📋 Estructura del Proyecto

```
SemestralA_SI/
├── index.html              # Dashboard principal
├── usuarios.html           # Gestión de usuarios
├── productos.html          # Gestión de productos
├── css/
│   ├── styles.css          # Estilos principales
│   └── pages.css           # Estilos de páginas específicas
├── js/
│   ├── main.js             # Funcionalidad principal
│   └── pages.js            # Funcionalidad de páginas
└── assets/
    └── images/             # Imágenes del proyecto
```

## 🛠️ Tecnologías Utilizadas

- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos con variables CSS y gradientes
- **JavaScript**: Interactividad y funcionalidad dinámica
- **Chart.js**: Gráficos interactivos
- **Font Awesome**: Iconos profesionales

## 🎨 Características de Diseño

### Variables CSS
El proyecto utiliza variables CSS para facilitar la personalización:
- Colores primarios y secundarios
- Modo claro y oscuro
- Sombras y bordes consistentes
- Transiciones suaves

### Componentes Principales
- **Sidebar**: Navegación lateral colapsable
- **Header**: Barra superior con búsqueda y notificaciones
- **Tarjetas de Estadísticas**: Métricas visuales con iconos
- **Gráficos**: Visualización de datos con Chart.js
- **Tablas**: Tablas de datos interactivas
- **Modales**: Formularios para crear/editar registros
- **Tarjetas de Productos**: Vista de cuadrícula para productos

## 📱 Responsive Design

El diseño se adapta a diferentes tamaños de pantalla:
- **Desktop**: Layout completo con sidebar y múltiples columnas
- **Tablet**: Layout adaptado con sidebar colapsable
- **Mobile**: Vista optimizada para dispositivos móviles

## 🔧 Funcionalidades JavaScript

### Dashboard (main.js)
- Toggle de sidebar
- Cambio de tema claro/oscuro
- Gráficos interactivos con Chart.js
- Animación de números en estadísticas
- Búsqueda en tiempo real

### Páginas (pages.js)
- Sistema de modales
- Validación de formularios
- Búsqueda y filtrado
- Paginación
- Confirmación de eliminación

## 🚀 Cómo Usar

1. **Abrir el proyecto**:
   ```bash
   # Simplemente abre index.html en tu navegador
   ```

2. **Navegación**:
   - Usa el menú lateral para navegar entre secciones
   - Click en el icono de hamburguesa para colapsar/expandir el sidebar
   - Usa el botón de luna/sol para cambiar el tema

3. **Funcionalidades**:
   - **Dashboard**: Visualiza estadísticas y actividad reciente
   - **Usuarios**: Gestiona usuarios, roles y permisos
   - **Productos**: Administra el catálogo de productos
   - **Búsqueda**: Usa la barra de búsqueda para filtrar resultados

## 🎯 Próximas Mejoras

- Integración con backend/API
- Autenticación de usuarios
- Base de datos real
- Exportación de reportes (PDF, Excel)
- Notificaciones en tiempo real
- Sistema de permisos avanzado
- Más gráficos y visualizaciones
- Modo de impresión optimizado

## 👨‍💻 Desarrollo

### Personalización de Colores

Edita las variables CSS en `css/styles.css`:

```css
:root {
    --primary-color: #4f46e5;
    --secondary-color: #7c3aed;
    /* Más variables... */
}
```

### Agregar Nuevas Páginas

1. Crea un nuevo archivo HTML
2. Copia la estructura de `usuarios.html` o `productos.html`
3. Actualiza el contenido según necesites
4. Agrega el enlace en el sidebar de todas las páginas

## 📄 Licencia

Este proyecto es parte de un trabajo semestral académico.

## 🤝 Contribuciones

Este es un proyecto académico. Para sugerencias o mejoras, contacta al desarrollador.

---

**Desarrollado con ❤️ para el curso de Sistemas de Información**
