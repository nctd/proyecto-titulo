-- Calcula lineas a despachar por tipos de venta
CREATE OR REPLACE PROCEDURE SP_DATOS_REPORTE_VENTA(v_tipo_venta VARCHAR2,v_cant_lineas OUT NUMBER, v_valor OUT NUMBER,
                                             v_porc_linea OUT NUMBER,v_porc_valor OUT NUMBER) IS        
    v_total_lineas NUMBER;
    v_total_valor NUMBER;
BEGIN
    SELECT COUNT(num_linea),SUM(valor)
    INTO v_total_lineas,v_total_valor
    FROM linea l JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE UPPER(ov.tipo_venta) = UPPER(v_tipo_venta) AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    SELECT SUM(NVL(valor,0))
    INTO v_valor
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE UPPER(ov.tipo_venta) = UPPER(v_tipo_venta) AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    IF v_valor IS NULL THEN
        v_valor := 0;
    END IF;

    BEGIN
        v_porc_linea := ROUND(v_cant_lineas * 100 / v_total_lineas);
        EXCEPTION WHEN zero_divide THEN
        v_porc_linea := 0;     
    END;
    
    
    BEGIN
        v_porc_valor := ROUND(v_valor * 100 / v_total_valor);
        EXCEPTION WHEN zero_divide THEN
        v_porc_valor := 0;
    END;
END;

-- Calcula lineas a despachar por tipos de despacho
CREATE OR REPLACE PROCEDURE SP_DATOS_REPORTE_DESPACHO(v_tipo_despacho VARCHAR2,v_cant_lineas OUT NUMBER, v_valor OUT NUMBER,
                                             v_porc_linea OUT NUMBER,v_porc_valor OUT NUMBER) IS        
    v_total_lineas NUMBER;
    v_total_valor NUMBER;
BEGIN
    SELECT COUNT(num_linea),SUM(valor)
    INTO v_total_lineas,v_total_valor
    FROM linea l JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE UPPER(ov.tipo_despacho) = UPPER(v_tipo_despacho) AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    SELECT SUM(NVL(valor,0))
    INTO v_valor
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE UPPER(ov.tipo_despacho) = UPPER(v_tipo_despacho) AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');

    
    IF v_valor IS NULL THEN
        v_valor := 0;
    END IF;

    BEGIN
        v_porc_linea := ROUND(v_cant_lineas * 100 / v_total_lineas);
        EXCEPTION WHEN zero_divide THEN
        v_porc_linea := 0;     
    END;
    
    
    BEGIN
        v_porc_valor := ROUND(v_valor * 100 / v_total_valor);
        EXCEPTION WHEN zero_divide THEN
        v_porc_valor := 0;
    END;
END;

-- Procedimiento para obtener los valores de estado por carga segun el estado
CREATE OR REPLACE PROCEDURE SP_ESTADO_CARGA(v_estado VARCHAR2, v_cant_lineas OUT NUMBER, v_porc_estado OUT NUMBER) IS
    v_total_lineas NUMBER;
    
BEGIN
    SELECT COUNT(num_linea)
    INTO v_total_lineas
    FROM linea l JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');

    SELECT COUNT(num_linea)
    INTO v_cant_lineas
    FROM linea l JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE UPPER(estado) = UPPER(v_estado)
    AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');

    BEGIN 
        v_porc_estado := ROUND(v_cant_lineas * 100 / v_total_lineas);
        EXCEPTION WHEN ZERO_DIVIDE THEN
        v_porc_estado := 0;
    END;
END;


-- Calcula progreso diario de despacho por tipo de venta
CREATE OR REPLACE PROCEDURE SP_OBTENER_PROGRESO_DIARIO_VENTA(v_tipo_venta VARCHAR2, v_cant_lineas OUT NUMBER, 
                                                             v_cant_lineas_exitosas OUT NUMBER,
                                                             v_porc_exito_linea OUT NUMBER) IS

BEGIN    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY')
    AND UPPER(ov.tipo_venta) = UPPER(v_tipo_venta);
    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas_exitosas
    FROM linea l JOIN despacho dp ON(l.despacho_id = dp.id_despacho)
    JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE dp.guia_despacho IS NOT NULL AND dp.guia_despacho LIKE 'GD%'
    AND UPPER(ov.tipo_venta) = UPPER(v_tipo_venta)
    AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY'); 
    
    BEGIN
        v_porc_exito_linea := ROUND(v_cant_lineas_exitosas * 100 / v_cant_lineas);
        EXCEPTION WHEN ZERO_DIVIDE THEN
        v_porc_exito_linea := 0;
    END;
END;

-- Calcula progreso diario de despacho por tipo de despacho
CREATE OR REPLACE PROCEDURE SP_OBTENER_PROGRESO_DIARIO_DESPACHO(v_tipo_despacho VARCHAR2, v_cant_lineas OUT NUMBER, 
                                                             v_cant_lineas_exitosas OUT NUMBER,
                                                             v_porc_exito_linea OUT NUMBER) IS

BEGIN    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas
    FROM linea l JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY')
    AND UPPER(ov.tipo_despacho) = UPPER(v_tipo_despacho);
    
    SELECT COUNT(num_linea)
    INTO v_cant_lineas_exitosas
    FROM linea l JOIN despacho dp ON(l.despacho_id = dp.id_despacho)
    JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE dp.guia_despacho IS NOT NULL AND dp.guia_despacho LIKE 'GD%'
    AND UPPER(ov.tipo_despacho) = UPPER(v_tipo_despacho) 
    AND l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY'); 
     
    
    
    BEGIN
        v_porc_exito_linea := ROUND(v_cant_lineas_exitosas * 100 / v_cant_lineas);
        EXCEPTION WHEN ZERO_DIVIDE THEN
        v_porc_exito_linea := 0;
    END;
END;


-- Procedimiento que obtiene el total de lineas y lineas exitosas acorde a su progreso diario
CREATE OR REPLACE PROCEDURE SP_OBTENER_TOTAL_PROGRESO(v_total_lineas OUT NUMBER, v_total_lineas_exitosas OUT NUMBER, v_porc_exito OUT NUMBER) IS

BEGIN
    SELECT COUNT(num_linea)
    INTO v_total_lineas
    FROM linea l JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY');
    
    SELECT COUNT(num_linea)
    INTO v_total_lineas_exitosas
    FROM linea l JOIN despacho dp ON(l.despacho_id = dp.id_despacho)
    JOIN orden_venta ov ON(l.orden_venta_id = ov.orden_venta)
    JOIN planificacion p ON l.orden_venta_id = p.orden_venta_id
    WHERE l.orden_venta_id||num_linea = llave_busqueda
    AND TO_CHAR(fecha_planificacion,'DD/MM/YYYY') = TO_CHAR(SYSDATE,'DD/MM/YYYY')
    AND dp.guia_despacho IS NOT NULL AND dp.guia_despacho LIKE 'GD%';
    
    BEGIN
        v_porc_exito := ROUND(v_total_lineas_exitosas * 100 / v_total_lineas);
        EXCEPTION WHEN ZERO_DIVIDE THEN
        v_porc_exito := 0;
    END;

END;


-- Procedimiento para guardar el progreso diario por tipo de venta
CREATE OR REPLACE PROCEDURE SP_GUARDAR_PROGRESO_TIPO_VENTA IS
    v_cant_despacho NUMBER;
    v_cant_exitosos NUMBER;
    v_porc NUMBER;
    v_existe NUMBER;

    CURSOR cur_ventas IS
        SELECT DISTINCT tipo_venta
        FROM orden_venta;

BEGIN
    FOR reg_venta IN cur_ventas LOOP
        SELECT COUNT(fecha)
        INTO v_existe
        FROM indicador_tipo_venta
        WHERE TO_CHAR(fecha,'DD/MM/YY') = TO_CHAR(SYSDATE,'DD/MM/YY') AND UPPER(tipo_venta) = reg_venta.tipo_venta;
        
        IF v_existe = 0 THEN
            SP_OBTENER_PROGRESO_DIARIO_VENTA(reg_venta.tipo_venta,v_cant_despacho,v_cant_exitosos,v_porc);
            INSERT INTO INDICADOR_TIPO_VENTA
            VALUES(ISEQ$$_116469.NEXTVAL,reg_venta.tipo_venta,v_cant_despacho,v_cant_exitosos,v_porc,TO_CHAR(SYSDATE,'DD/MM/YY'),0);
        END IF;
    END LOOP;
END;


BEGIN
  SYS.DBMS_SCHEDULER.CREATE_JOB
    (
       job_name        => 'JOB_GUARDAR_PROGRESO_DIARIO_VENTAS'
      ,job_type        => 'PLSQL_BLOCK'
      ,start_date      => TO_TIMESTAMP_TZ('10/06/2021 12:23:00.000 PM -08:00','mm/dd/yyyy hh12:mi:ss.ff AM tzr')
      ,repeat_interval => 'FREQ=MINUTELY;INTERVAL=1'
      ,end_date        => TO_TIMESTAMP_TZ('12/31/2031 12:00:00.000 AM -08:00','mm/dd/yyyy hh12:mi:ss.ff AM tzr')
      ,auto_drop       => TRUE
      ,job_action      => '
                            BEGIN
                                SP_GUARDAR_PROGRESO_TIPO_VENTA();
                            END;
                          '
      ,comments        => 'Job que guarda el progreso diario de las ventas cada 24 horas.'
    );
END;


BEGIN
    DBMS_SCHEDULER.ENABLE
        (name => 'JOB_GUARDAR_PROGRESO_DIARIO_VENTAS');
END;



-- Procedimiento almacenado que guarda el progreso diario de despachos 
-- en la tabla INDICADOR_DESPACHO
CREATE OR REPLACE PROCEDURE SP_GUARDAR_PROGRESO_TIPO_DESPACHO IS
    v_cant_despacho NUMBER;
    v_cant_exitosos NUMBER;
    v_porc NUMBER;
    v_existe NUMBER;
    
    CURSOR cur_despachos IS
        SELECT DISTINCT tipo_despacho
        FROM orden_venta;
BEGIN
    FOR reg_despacho IN cur_despachos LOOP
        SELECT COUNT(fecha)
        INTO v_existe
        FROM INDICADOR_DESPACHO
        WHERE TO_CHAR(fecha,'DD/MM/YY') = TO_CHAR(SYSDATE,'DD/MM/YY') AND UPPER(tipo_despacho) = reg_despacho.tipo_despacho;
        
        IF v_existe = 0 THEN
            SP_OBTENER_PROGRESO_DIARIO_DESPACHO(reg_despacho.tipo_despacho,v_cant_despacho,v_cant_exitosos,v_porc);
            INSERT INTO INDICADOR_DESPACHO
            VALUES(ISEQ$$_109734.NEXTVAL,reg_despacho.tipo_despacho,v_cant_despacho,v_cant_exitosos,v_porc,TO_CHAR(SYSDATE,'DD/MM/YY'),0);
            --ELSE
                --RAISE EXCEPTION 
        END IF;
    END LOOP;

END;


BEGIN
  SYS.DBMS_SCHEDULER.CREATE_JOB
    (
       job_name        => 'JOB_GUARDAR_PROGRESO_DIARIO_DESPACHOS'
      ,job_type        => 'PLSQL_BLOCK'
      ,start_date      => TO_TIMESTAMP_TZ('10/06/2021 12:23:00.000 PM -08:00','mm/dd/yyyy hh12:mi:ss.ff AM tzr')
      ,repeat_interval => 'FREQ=MINUTELY;INTERVAL=1'
      ,end_date        => TO_TIMESTAMP_TZ('12/31/2031 12:00:00.000 AM -08:00','mm/dd/yyyy hh12:mi:ss.ff AM tzr')
      ,auto_drop       => TRUE
      ,job_action      => '
                            BEGIN
                                SP_GUARDAR_PROGRESO_TIPO_DESPACHO();
                            END;
                          '
      ,comments        => 'Job que guarda el progreso diario de los despachos cada 24 horas.'
    );
END;


BEGIN
    DBMS_SCHEDULER.ENABLE
        (name => 'JOB_GUARDAR_PROGRESO_DIARIO_DESPACHOS');
END;
