-- Script para agregar las columnas faltantes a la tabla USUARIO
-- Ejecutar este script en MySQL Workbench o mediante el shell de Django

-- Agregar USU_IS_STAFF si no existe
ALTER TABLE USUARIO 
ADD COLUMN IF NOT EXISTS USU_IS_STAFF TINYINT(1) NOT NULL DEFAULT 0;

-- Agregar USU_IS_SUPERUSER si no existe
ALTER TABLE USUARIO 
ADD COLUMN IF NOT EXISTS USU_IS_SUPERUSER TINYINT(1) NOT NULL DEFAULT 0;

-- Verificar las columnas
DESCRIBE USUARIO;
