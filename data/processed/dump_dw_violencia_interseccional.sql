-- =============================================================================
-- ENTREGÁVEL 3: DUMP SQL COMPLETO DO BANCO DE DADOS (STAR SCHEMA + DADOS)
-- Banco: dw_violencia_interseccional (ODS 5 & ODS 18 - Capitais 2025)
-- =============================================================================

BEGIN TRANSACTION;
CREATE TABLE dim_contexto_crime (
        id_contexto         INTEGER PRIMARY KEY,
        fonte_dados         VARCHAR(30) NOT NULL,
        tipo_evento         VARCHAR(150) NOT NULL,
        arma                VARCHAR(80) NOT NULL,
        agente_seguranca    VARCHAR(80) NOT NULL,
        acao_policial       BOOLEAN NOT NULL DEFAULT 0,
        presenca_agente     BOOLEAN NOT NULL DEFAULT 0,
        chacina             BOOLEAN NOT NULL DEFAULT 0,
        circunstancia       VARCHAR(100) NOT NULL DEFAULT 'Não especificada',
        local_ocorrencia    VARCHAR(100) NOT NULL DEFAULT 'Não especificado',
        UNIQUE (fonte_dados, tipo_evento, arma, agente_seguranca, acao_policial, presenca_agente, chacina, circunstancia, local_ocorrencia)
    );
INSERT INTO "dim_contexto_crime" VALUES(1,'SINESP_MJSP','Feminicídio','Não informada','Não informado',0,0,0,'Registro Oficial SINESP (Capitais 2025)','Estadual');
INSERT INTO "dim_contexto_crime" VALUES(2,'SINESP_MJSP','Tentativa de feminicídio','Não informada','Não informado',0,0,0,'Registro Oficial SINESP (Capitais 2025)','Estadual');
INSERT INTO "dim_contexto_crime" VALUES(3,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(4,'FOGO_CRUZADO','Tentativa/Roubo','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Outros');
INSERT INTO "dim_contexto_crime" VALUES(5,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Residência');
INSERT INTO "dim_contexto_crime" VALUES(6,'FOGO_CRUZADO','Tentativa/Roubo','Arma de fogo','Agente de Segurança Presente',1,1,0,'Bala perdida','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(7,'FOGO_CRUZADO','Tiros a esmo','Arma de fogo','Sem Agente Identificado',0,0,1,'Chacina','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(8,'FOGO_CRUZADO','Ação policial','Arma de fogo','Agente de Segurança Presente',1,1,0,'Bala perdida','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(9,'FOGO_CRUZADO','Disparo Acidental','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Evento');
INSERT INTO "dim_contexto_crime" VALUES(10,'FOGO_CRUZADO','Não identificado','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(11,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Evento');
INSERT INTO "dim_contexto_crime" VALUES(12,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,1,'Chacina','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(13,'FOGO_CRUZADO','Briga','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(14,'FOGO_CRUZADO','Briga','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Bar');
INSERT INTO "dim_contexto_crime" VALUES(15,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Agente de Segurança Presente',0,1,0,'Transfeminicídio; Sem identificação','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(16,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Feminicídio/tentativa','Residência');
INSERT INTO "dim_contexto_crime" VALUES(17,'FOGO_CRUZADO','Tortura','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Residência');
INSERT INTO "dim_contexto_crime" VALUES(18,'FOGO_CRUZADO','Ação policial','Arma de fogo','Agente de Segurança Presente',1,1,0,'Bala perdida','Residência');
INSERT INTO "dim_contexto_crime" VALUES(19,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Feminicídio/tentativa','Outros');
INSERT INTO "dim_contexto_crime" VALUES(20,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Agente de Segurança Presente',0,1,0,'Feminicídio/tentativa','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(21,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Feminicídio/tentativa','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(22,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Feminicídio/tentativa','Bar');
INSERT INTO "dim_contexto_crime" VALUES(23,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Encontro de cadáver','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(24,'FOGO_CRUZADO','Briga','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Outros');
INSERT INTO "dim_contexto_crime" VALUES(25,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,1,'Chacina','Evento');
INSERT INTO "dim_contexto_crime" VALUES(26,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Outros');
INSERT INTO "dim_contexto_crime" VALUES(27,'FOGO_CRUZADO','Tentativa/Roubo','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(28,'FOGO_CRUZADO','Operação policial','Arma de fogo','Agente de Segurança Presente',1,1,1,'Chacina; Bala perdida','Residência');
INSERT INTO "dim_contexto_crime" VALUES(29,'FOGO_CRUZADO','Tentativa/Roubo','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(30,'FOGO_CRUZADO','Tentativa/Roubo','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Bar');
INSERT INTO "dim_contexto_crime" VALUES(31,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Evento');
INSERT INTO "dim_contexto_crime" VALUES(32,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(33,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(34,'FOGO_CRUZADO','Ação policial','Arma de fogo','Agente de Segurança Presente',1,1,0,'Sem identificação','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(35,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Sem identificação');
INSERT INTO "dim_contexto_crime" VALUES(36,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(37,'FOGO_CRUZADO','Disputa','Arma de fogo','Sem Agente Identificado',0,0,0,'Bala perdida','Outros');
INSERT INTO "dim_contexto_crime" VALUES(38,'FOGO_CRUZADO','Ataque a civis','Arma de fogo','Sem Agente Identificado',0,0,0,'Sem identificação','Automóvel');
INSERT INTO "dim_contexto_crime" VALUES(39,'FOGO_CRUZADO','Homicidio/Tentativa','Arma de fogo','Sem Agente Identificado',0,0,0,'Feminicídio/tentativa','Unidade de ensino');
CREATE TABLE dim_localidade (
        id_localidade   INTEGER PRIMARY KEY,
        regiao          VARCHAR(20) NOT NULL,
        uf              CHAR(2) NOT NULL,
        estado          VARCHAR(50) NOT NULL,
        municipio       VARCHAR(120) NOT NULL,
        bairro          VARCHAR(120) DEFAULT 'NÃO ESPECIFICADO',
        UNIQUE (uf, municipio, bairro)
    );
INSERT INTO "dim_localidade" VALUES(1,'Centro-Oeste','DF','Distrito Federal','BRASÍLIA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(2,'Centro-Oeste','GO','Goiás','GOIÂNIA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(3,'Centro-Oeste','MS','Mato Grosso do Sul','CAMPO GRANDE','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(4,'Centro-Oeste','MT','Mato Grosso','CUIABÁ','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(5,'Nordeste','AL','Alagoas','MACEIÓ','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(6,'Nordeste','BA','Bahia','SALVADOR','AGUAS CLARAS');
INSERT INTO "dim_localidade" VALUES(7,'Nordeste','BA','Bahia','SALVADOR','ALTO DO CABRITO');
INSERT INTO "dim_localidade" VALUES(8,'Nordeste','BA','Bahia','SALVADOR','BROTAS');
INSERT INTO "dim_localidade" VALUES(9,'Nordeste','BA','Bahia','SALVADOR','CALCADA');
INSERT INTO "dim_localidade" VALUES(10,'Nordeste','BA','Bahia','SALVADOR','CENTRO');
INSERT INTO "dim_localidade" VALUES(11,'Nordeste','BA','Bahia','SALVADOR','COSME DE FARIAS');
INSERT INTO "dim_localidade" VALUES(12,'Nordeste','BA','Bahia','SALVADOR','ENGENHO VELHO DA FEDERACAO');
INSERT INTO "dim_localidade" VALUES(13,'Nordeste','BA','Bahia','SALVADOR','ENGENHO VELHO DE BROTAS');
INSERT INTO "dim_localidade" VALUES(14,'Nordeste','BA','Bahia','SALVADOR','ENGOMADEIRA');
INSERT INTO "dim_localidade" VALUES(15,'Nordeste','BA','Bahia','SALVADOR','IAPI');
INSERT INTO "dim_localidade" VALUES(16,'Nordeste','BA','Bahia','SALVADOR','JARDIM DAS MARGARIDAS');
INSERT INTO "dim_localidade" VALUES(17,'Nordeste','BA','Bahia','SALVADOR','JARDIM SANTO INACIO');
INSERT INTO "dim_localidade" VALUES(18,'Nordeste','BA','Bahia','SALVADOR','LOBATO');
INSERT INTO "dim_localidade" VALUES(19,'Nordeste','BA','Bahia','SALVADOR','MASSARANDUBA');
INSERT INTO "dim_localidade" VALUES(20,'Nordeste','BA','Bahia','SALVADOR','MORADAS DA LAGOA');
INSERT INTO "dim_localidade" VALUES(21,'Nordeste','BA','Bahia','SALVADOR','NORDESTE DE AMARALINA');
INSERT INTO "dim_localidade" VALUES(22,'Nordeste','BA','Bahia','SALVADOR','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(23,'Nordeste','BA','Bahia','SALVADOR','PAU DA LIMA');
INSERT INTO "dim_localidade" VALUES(24,'Nordeste','BA','Bahia','SALVADOR','PAU MIUDO');
INSERT INTO "dim_localidade" VALUES(25,'Nordeste','BA','Bahia','SALVADOR','PERIPERI');
INSERT INTO "dim_localidade" VALUES(26,'Nordeste','BA','Bahia','SALVADOR','SAO CRISTOVAO');
INSERT INTO "dim_localidade" VALUES(27,'Nordeste','BA','Bahia','SALVADOR','SETE DE ABRIL');
INSERT INTO "dim_localidade" VALUES(28,'Nordeste','BA','Bahia','SALVADOR','TROBOGY');
INSERT INTO "dim_localidade" VALUES(29,'Nordeste','BA','Bahia','SALVADOR','VALE DOS LAGOS');
INSERT INTO "dim_localidade" VALUES(30,'Nordeste','BA','Bahia','SALVADOR','VILA LAURA');
INSERT INTO "dim_localidade" VALUES(31,'Nordeste','CE','Ceará','FORTALEZA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(32,'Nordeste','MA','Maranhão','SÃO LUÍS','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(33,'Nordeste','PB','Paraíba','JOÃO PESSOA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(34,'Nordeste','PE','Pernambuco','RECIFE','AFOGADOS');
INSERT INTO "dim_localidade" VALUES(35,'Nordeste','PE','Pernambuco','RECIFE','AGUA FRIA');
INSERT INTO "dim_localidade" VALUES(36,'Nordeste','PE','Pernambuco','RECIFE','BOMBA DO HEMETERIO');
INSERT INTO "dim_localidade" VALUES(37,'Nordeste','PE','Pernambuco','RECIFE','BREJO DA GUABIRABA');
INSERT INTO "dim_localidade" VALUES(38,'Nordeste','PE','Pernambuco','RECIFE','BREJO DE BEBERIBE');
INSERT INTO "dim_localidade" VALUES(39,'Nordeste','PE','Pernambuco','RECIFE','CASA AMARELA');
INSERT INTO "dim_localidade" VALUES(40,'Nordeste','PE','Pernambuco','RECIFE','COHAB');
INSERT INTO "dim_localidade" VALUES(41,'Nordeste','PE','Pernambuco','RECIFE','CORDEIRO');
INSERT INTO "dim_localidade" VALUES(42,'Nordeste','PE','Pernambuco','RECIFE','DOIS UNIDOS');
INSERT INTO "dim_localidade" VALUES(43,'Nordeste','PE','Pernambuco','RECIFE','IBURA');
INSERT INTO "dim_localidade" VALUES(44,'Nordeste','PE','Pernambuco','RECIFE','IPUTINGA');
INSERT INTO "dim_localidade" VALUES(45,'Nordeste','PE','Pernambuco','RECIFE','MACAXEIRA');
INSERT INTO "dim_localidade" VALUES(46,'Nordeste','PE','Pernambuco','RECIFE','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(47,'Nordeste','PE','Pernambuco','RECIFE','PASSARINHO');
INSERT INTO "dim_localidade" VALUES(48,'Nordeste','PE','Pernambuco','RECIFE','PORTO DA MADEIRA');
INSERT INTO "dim_localidade" VALUES(49,'Nordeste','PE','Pernambuco','RECIFE','SAN MARTIN');
INSERT INTO "dim_localidade" VALUES(50,'Nordeste','PE','Pernambuco','RECIFE','SAO JOSE');
INSERT INTO "dim_localidade" VALUES(51,'Nordeste','PE','Pernambuco','RECIFE','TORRE');
INSERT INTO "dim_localidade" VALUES(52,'Nordeste','PE','Pernambuco','RECIFE','TORROES');
INSERT INTO "dim_localidade" VALUES(53,'Nordeste','PE','Pernambuco','RECIFE','VARZEA');
INSERT INTO "dim_localidade" VALUES(54,'Nordeste','PI','Piauí','TERESINA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(55,'Nordeste','RN','Rio Grande do Norte','NATAL','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(56,'Nordeste','SE','Sergipe','ARACAJU','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(57,'Norte','AC','Acre','RIO BRANCO','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(58,'Norte','AM','Amazonas','MANAUS','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(59,'Norte','AP','Amapá','MACAPÁ','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(60,'Norte','PA','Pará','BELÉM','GUAMA');
INSERT INTO "dim_localidade" VALUES(61,'Norte','PA','Pará','BELÉM','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(62,'Norte','PA','Pará','BELÉM','PEDREIRA');
INSERT INTO "dim_localidade" VALUES(63,'Norte','RO','Rondônia','PORTO VELHO','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(64,'Norte','RR','Roraima','BOA VISTA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(65,'Norte','TO','Tocantins','PALMAS','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(66,'Sudeste','ES','Espírito Santo','VITÓRIA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(67,'Sudeste','MG','Minas Gerais','BELO HORIZONTE','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(68,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','BANGU');
INSERT INTO "dim_localidade" VALUES(69,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','CAJU');
INSERT INTO "dim_localidade" VALUES(70,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','CASCADURA');
INSERT INTO "dim_localidade" VALUES(71,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','CATETE');
INSERT INTO "dim_localidade" VALUES(72,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','CURICICA');
INSERT INTO "dim_localidade" VALUES(73,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','GARDENIA AZUL');
INSERT INTO "dim_localidade" VALUES(74,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','INHOAIBA');
INSERT INTO "dim_localidade" VALUES(75,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','IRAJA');
INSERT INTO "dim_localidade" VALUES(76,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','JARDIM SULACAP');
INSERT INTO "dim_localidade" VALUES(77,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','MARACANA');
INSERT INTO "dim_localidade" VALUES(78,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(79,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','PENHA');
INSERT INTO "dim_localidade" VALUES(80,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','SEPETIBA');
INSERT INTO "dim_localidade" VALUES(81,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','TAUA');
INSERT INTO "dim_localidade" VALUES(82,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','TIJUCA');
INSERT INTO "dim_localidade" VALUES(83,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','VIGARIO GERAL');
INSERT INTO "dim_localidade" VALUES(84,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','VILA KENNEDY');
INSERT INTO "dim_localidade" VALUES(85,'Sudeste','RJ','Rio de Janeiro','RIO DE JANEIRO','VILA VALQUEIRE');
INSERT INTO "dim_localidade" VALUES(86,'Sudeste','SP','São Paulo','SÃO PAULO','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(87,'Sul','PR','Paraná','CURITIBA','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(88,'Sul','RS','Rio Grande do Sul','PORTO ALEGRE','NÃO ESPECIFICADO');
INSERT INTO "dim_localidade" VALUES(89,'Sul','SC','Santa Catarina','FLORIANÓPOLIS','NÃO ESPECIFICADO');
CREATE TABLE dim_perfil_vitima (
        id_perfil               INTEGER PRIMARY KEY,
        genero                  VARCHAR(45) NOT NULL,
        macro_genero            VARCHAR(25) NOT NULL,
        raca_cor                VARCHAR(35) NOT NULL,
        faixa_etaria            VARCHAR(45) NOT NULL,
        tipo_pessoa             VARCHAR(35) NOT NULL,
        grupo_interseccional    VARCHAR(80) NOT NULL,
        UNIQUE (genero, raca_cor, faixa_etaria, tipo_pessoa)
    );
INSERT INTO "dim_perfil_vitima" VALUES(1,'Mulher cis','Mulher Cis','Branca','Adulta (25-34)','Civil','Mulher cis - Branca');
INSERT INTO "dim_perfil_vitima" VALUES(2,'Mulher cis','Mulher Cis','Branca','Adulta (35-45)','Civil','Mulher cis - Branca');
INSERT INTO "dim_perfil_vitima" VALUES(3,'Mulher cis','Mulher Cis','Branca','Jovem Adulta (18-24)','Civil','Mulher cis - Branca');
INSERT INTO "dim_perfil_vitima" VALUES(4,'Mulher cis','Mulher Cis','Negra','Adulta (25-34)','Civil','Mulher cis - Negra');
INSERT INTO "dim_perfil_vitima" VALUES(5,'Mulher cis','Mulher Cis','Negra','Adulta (35-45)','Civil','Mulher cis - Negra');
INSERT INTO "dim_perfil_vitima" VALUES(6,'Mulher cis','Mulher Cis','Negra','Jovem Adulta (18-24)','Civil','Mulher cis - Negra');
INSERT INTO "dim_perfil_vitima" VALUES(7,'Mulher cis','Mulher Cis','Não identificado','Adulta (25-34)','Civil','Mulher cis - Não identificado');
INSERT INTO "dim_perfil_vitima" VALUES(8,'Mulher cis','Mulher Cis','Não identificado','Adulta (35-45)','Civil','Mulher cis - Não identificado');
INSERT INTO "dim_perfil_vitima" VALUES(9,'Mulher cis','Mulher Cis','Não identificado','Jovem Adulta (18-24)','Civil','Mulher cis - Não identificado');
INSERT INTO "dim_perfil_vitima" VALUES(10,'Mulher trans e travesti','Mulher Trans/Travesti','Negra','Adulta (25-34)','Civil','Mulher trans e travesti - Negra');
INSERT INTO "dim_perfil_vitima" VALUES(11,'Mulher trans e travesti','Mulher Trans/Travesti','Negra','Jovem Adulta (18-24)','Civil','Mulher trans e travesti - Negra');
CREATE TABLE dim_tempo (
        id_tempo        INTEGER PRIMARY KEY,
        data_completa   DATE NOT NULL UNIQUE,
        ano             SMALLINT NOT NULL,
        mes             SMALLINT NOT NULL,
        nome_mes        VARCHAR(20) NOT NULL,
        trimestre       SMALLINT NOT NULL,
        semestre        SMALLINT NOT NULL
    );
INSERT INTO "dim_tempo" VALUES(20250101,'2025-01-01',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250108,'2025-01-08',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250112,'2025-01-12',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250115,'2025-01-15',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250120,'2025-01-20',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250124,'2025-01-24',2025,1,'Janeiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250201,'2025-02-01',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250209,'2025-02-09',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250212,'2025-02-12',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250214,'2025-02-14',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250221,'2025-02-21',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250226,'2025-02-26',2025,2,'Fevereiro',1,1);
INSERT INTO "dim_tempo" VALUES(20250301,'2025-03-01',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250303,'2025-03-03',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250309,'2025-03-09',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250310,'2025-03-10',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250312,'2025-03-12',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250314,'2025-03-14',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250315,'2025-03-15',2025,3,'Março',1,1);
INSERT INTO "dim_tempo" VALUES(20250401,'2025-04-01',2025,4,'Abril',2,1);
INSERT INTO "dim_tempo" VALUES(20250408,'2025-04-08',2025,4,'Abril',2,1);
INSERT INTO "dim_tempo" VALUES(20250413,'2025-04-13',2025,4,'Abril',2,1);
INSERT INTO "dim_tempo" VALUES(20250419,'2025-04-19',2025,4,'Abril',2,1);
INSERT INTO "dim_tempo" VALUES(20250426,'2025-04-26',2025,4,'Abril',2,1);
INSERT INTO "dim_tempo" VALUES(20250501,'2025-05-01',2025,5,'Maio',2,1);
INSERT INTO "dim_tempo" VALUES(20250507,'2025-05-07',2025,5,'Maio',2,1);
INSERT INTO "dim_tempo" VALUES(20250513,'2025-05-13',2025,5,'Maio',2,1);
INSERT INTO "dim_tempo" VALUES(20250528,'2025-05-28',2025,5,'Maio',2,1);
INSERT INTO "dim_tempo" VALUES(20250529,'2025-05-29',2025,5,'Maio',2,1);
INSERT INTO "dim_tempo" VALUES(20250601,'2025-06-01',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250608,'2025-06-08',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250615,'2025-06-15',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250617,'2025-06-17',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250624,'2025-06-24',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250628,'2025-06-28',2025,6,'Junho',2,1);
INSERT INTO "dim_tempo" VALUES(20250701,'2025-07-01',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250705,'2025-07-05',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250713,'2025-07-13',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250717,'2025-07-17',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250722,'2025-07-22',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250725,'2025-07-25',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250726,'2025-07-26',2025,7,'Julho',3,2);
INSERT INTO "dim_tempo" VALUES(20250801,'2025-08-01',2025,8,'Agosto',3,2);
INSERT INTO "dim_tempo" VALUES(20250810,'2025-08-10',2025,8,'Agosto',3,2);
INSERT INTO "dim_tempo" VALUES(20250814,'2025-08-14',2025,8,'Agosto',3,2);
INSERT INTO "dim_tempo" VALUES(20250817,'2025-08-17',2025,8,'Agosto',3,2);
INSERT INTO "dim_tempo" VALUES(20250820,'2025-08-20',2025,8,'Agosto',3,2);
INSERT INTO "dim_tempo" VALUES(20250901,'2025-09-01',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250904,'2025-09-04',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250905,'2025-09-05',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250918,'2025-09-18',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250925,'2025-09-25',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250927,'2025-09-27',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20250928,'2025-09-28',2025,9,'Setembro',3,2);
INSERT INTO "dim_tempo" VALUES(20251001,'2025-10-01',2025,10,'Outubro',4,2);
INSERT INTO "dim_tempo" VALUES(20251006,'2025-10-06',2025,10,'Outubro',4,2);
INSERT INTO "dim_tempo" VALUES(20251012,'2025-10-12',2025,10,'Outubro',4,2);
INSERT INTO "dim_tempo" VALUES(20251024,'2025-10-24',2025,10,'Outubro',4,2);
INSERT INTO "dim_tempo" VALUES(20251101,'2025-11-01',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251104,'2025-11-04',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251105,'2025-11-05',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251114,'2025-11-14',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251117,'2025-11-17',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251122,'2025-11-22',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251123,'2025-11-23',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251128,'2025-11-28',2025,11,'Novembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251201,'2025-12-01',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251207,'2025-12-07',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251218,'2025-12-18',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251220,'2025-12-20',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251223,'2025-12-23',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251224,'2025-12-24',2025,12,'Dezembro',4,2);
INSERT INTO "dim_tempo" VALUES(20251228,'2025-12-28',2025,12,'Dezembro',4,2);
CREATE TABLE fato_violencia_sinesp (
        id_fato_sinesp      INTEGER PRIMARY KEY,
        id_tempo            INTEGER NOT NULL REFERENCES dim_tempo(id_tempo),
        id_localidade       INTEGER NOT NULL REFERENCES dim_localidade(id_localidade),
        id_contexto         INTEGER NOT NULL REFERENCES dim_contexto_crime(id_contexto),
        vitimas_feminino    INTEGER NOT NULL DEFAULT 0,
        vitimas_masculino   INTEGER NOT NULL DEFAULT 0,
        vitimas_nao_inf     INTEGER NOT NULL DEFAULT 0,
        total_vitimas       INTEGER NOT NULL DEFAULT 0,
        total_ocorrencias   NUMERIC(12, 2) NOT NULL DEFAULT 0,
        total_peso          NUMERIC(12, 3) NOT NULL DEFAULT 0
    );
INSERT INTO "fato_violencia_sinesp" VALUES(1,20250401,57,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(2,20250801,57,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(3,20250901,57,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(4,20251201,57,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(5,20250101,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(6,20250301,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(7,20250401,57,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(8,20250501,57,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(9,20250601,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(10,20250701,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(11,20250801,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(12,20250901,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(13,20251101,57,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(14,20251201,57,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(15,20250501,5,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(16,20250801,5,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(17,20251001,5,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(18,20251101,5,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(19,20251201,5,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(20,20250101,5,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(21,20250201,5,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(22,20250301,5,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(23,20250601,5,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(24,20251101,5,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(25,20250501,58,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(26,20250601,58,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(27,20250701,58,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(28,20250801,58,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(29,20251001,58,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(30,20251201,58,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(31,20250101,58,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(32,20250201,58,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(33,20250301,58,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(34,20250401,58,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(35,20250501,58,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(36,20250601,58,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(37,20250701,58,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(38,20250801,58,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(39,20250901,58,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(40,20251001,58,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(41,20251101,58,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(42,20251201,58,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(43,20250601,59,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(44,20251101,59,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(45,20250101,59,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(46,20250201,59,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(47,20250301,59,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(48,20250501,59,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(49,20250601,59,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(50,20250701,59,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(51,20250801,59,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(52,20250901,59,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(53,20251001,59,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(54,20251101,59,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(55,20251201,59,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(56,20250101,22,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(57,20250201,22,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(58,20250301,22,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(59,20250401,22,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(60,20250801,22,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(61,20250901,22,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(62,20251201,22,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(63,20250101,22,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(64,20250201,22,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(65,20250301,22,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(66,20250401,22,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(67,20250501,22,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(68,20250601,22,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(69,20250701,22,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(70,20250801,22,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(71,20250901,22,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(72,20251001,22,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(73,20251101,22,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(74,20251201,22,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(75,20250201,31,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(76,20250501,31,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(77,20250701,31,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(78,20250801,31,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(79,20250301,31,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(80,20250401,31,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(81,20250501,31,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(82,20250601,31,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(83,20250801,31,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(84,20251001,31,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(85,20251101,31,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(86,20251201,31,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(87,20250101,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(88,20250201,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(89,20250301,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(90,20250401,1,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(91,20250501,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(92,20250601,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(93,20250701,1,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(94,20250801,1,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(95,20250901,1,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(96,20251001,1,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(97,20251101,1,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(98,20251201,1,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(99,20250101,1,2,11,0,0,11,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(100,20250201,1,2,7,0,0,7,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(101,20250301,1,2,14,0,0,14,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(102,20250401,1,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(103,20250501,1,2,18,0,0,18,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(104,20250601,1,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(105,20250701,1,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(106,20250801,1,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(107,20250901,1,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(108,20251001,1,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(109,20251101,1,2,18,0,0,18,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(110,20251201,1,2,13,0,0,13,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(111,20250101,66,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(112,20250401,2,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(113,20250601,2,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(114,20251001,2,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(115,20251101,2,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(116,20251201,2,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(117,20250101,2,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(118,20250201,2,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(119,20250301,2,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(120,20250401,2,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(121,20250501,2,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(122,20250901,2,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(123,20251001,2,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(124,20251201,2,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(125,20250401,32,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(126,20250501,32,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(127,20250601,32,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(128,20250901,32,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(129,20250101,32,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(130,20250601,32,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(131,20250701,32,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(132,20250901,32,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(133,20251201,32,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(134,20250101,67,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(135,20250301,67,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(136,20250401,67,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(137,20250501,67,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(138,20250701,67,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(139,20250801,67,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(140,20251001,67,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(141,20251101,67,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(142,20251201,67,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(143,20250101,67,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(144,20250201,67,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(145,20250301,67,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(146,20250401,67,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(147,20250501,67,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(148,20250601,67,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(149,20250701,67,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(150,20250801,67,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(151,20250901,67,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(152,20251001,67,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(153,20251101,67,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(154,20251201,67,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(155,20250201,3,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(156,20250301,3,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(157,20250501,3,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(158,20251001,3,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(159,20251201,3,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(160,20250101,3,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(161,20250201,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(162,20250301,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(163,20250401,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(164,20250501,3,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(165,20250701,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(166,20250801,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(167,20250901,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(168,20251001,3,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(169,20251101,3,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(170,20250401,4,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(171,20250501,4,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(172,20250701,4,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(173,20250101,4,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(174,20250201,4,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(175,20250301,4,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(176,20250401,4,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(177,20250501,4,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(178,20250601,4,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(179,20250701,4,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(180,20250801,4,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(181,20250901,4,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(182,20251001,4,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(183,20251101,4,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(184,20251201,4,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(185,20250101,61,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(186,20250301,61,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(187,20250501,61,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(188,20251201,61,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(189,20250101,61,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(190,20250201,61,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(191,20250301,61,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(192,20250401,61,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(193,20250501,61,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(194,20250601,61,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(195,20250801,61,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(196,20250901,61,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(197,20251001,61,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(198,20251101,61,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(199,20251201,61,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(200,20250301,33,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(201,20250501,33,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(202,20250901,33,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(203,20251101,33,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(204,20251201,33,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(205,20250201,33,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(206,20250301,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(207,20250401,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(208,20250601,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(209,20250801,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(210,20251001,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(211,20251101,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(212,20251201,33,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(213,20250101,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(214,20250201,46,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(215,20250301,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(216,20250401,46,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(217,20250501,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(218,20250801,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(219,20251001,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(220,20251101,46,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(221,20251201,46,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(222,20250101,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(223,20250201,46,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(224,20250301,46,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(225,20250401,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(226,20250501,46,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(227,20250601,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(228,20250701,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(229,20250801,46,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(230,20250901,46,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(231,20251001,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(232,20251101,46,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(233,20251201,46,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(234,20250101,54,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(235,20250201,54,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(236,20250401,54,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(237,20250701,54,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(238,20250801,54,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(239,20251201,54,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(240,20250201,54,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(241,20250401,54,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(242,20250501,54,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(243,20250601,54,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(244,20250701,54,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(245,20250801,54,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(246,20250901,54,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(247,20251001,54,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(248,20251101,54,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(249,20251201,54,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(250,20250201,87,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(251,20250601,87,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(252,20250701,87,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(253,20250901,87,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(254,20251001,87,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(255,20251201,87,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(256,20250101,87,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(257,20250201,87,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(258,20250301,87,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(259,20250501,87,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(260,20250601,87,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(261,20250701,87,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(262,20250801,87,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(263,20250901,87,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(264,20251001,87,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(265,20251101,87,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(266,20251201,87,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(267,20250101,78,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(268,20250201,78,1,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(269,20250301,78,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(270,20250401,78,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(271,20250501,78,1,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(272,20250601,78,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(273,20250701,78,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(274,20250801,78,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(275,20250901,78,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(276,20251001,78,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(277,20251101,78,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(278,20251201,78,1,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(279,20250101,78,2,7,0,0,7,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(280,20250201,78,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(281,20250301,78,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(282,20250401,78,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(283,20250501,78,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(284,20250601,78,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(285,20250701,78,2,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(286,20250801,78,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(287,20250901,78,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(288,20251001,78,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(289,20251101,78,2,7,0,0,7,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(290,20251201,78,2,9,0,0,9,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(291,20250801,55,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(292,20250901,55,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(293,20250101,55,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(294,20250301,55,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(295,20250501,55,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(296,20250601,55,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(297,20250701,55,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(298,20250801,55,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(299,20250901,55,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(300,20251001,55,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(301,20251101,55,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(302,20251201,55,2,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(303,20250101,63,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(304,20250201,63,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(305,20250401,63,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(306,20250601,63,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(307,20250901,63,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(308,20250101,63,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(309,20250201,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(310,20250301,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(311,20250401,63,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(312,20250501,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(313,20250701,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(314,20250801,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(315,20250901,63,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(316,20251001,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(317,20251101,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(318,20251201,63,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(319,20250501,64,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(320,20251001,64,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(321,20250101,64,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(322,20250301,64,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(323,20250401,64,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(324,20250501,64,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(325,20250601,64,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(326,20250701,64,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(327,20250801,64,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(328,20250901,64,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(329,20251001,64,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(330,20251201,64,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(331,20250101,88,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(332,20250801,88,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(333,20250901,88,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(334,20251201,88,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(335,20250101,88,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(336,20250201,88,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(337,20250301,88,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(338,20250401,88,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(339,20250501,88,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(340,20250601,88,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(341,20250701,88,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(342,20250801,88,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(343,20250901,88,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(344,20251001,88,2,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(345,20251101,88,2,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(346,20251201,88,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(347,20250401,89,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(348,20250801,89,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(349,20250901,89,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(350,20251101,89,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(351,20250101,89,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(352,20250201,89,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(353,20250301,89,2,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(354,20250401,89,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(355,20250801,89,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(356,20251001,89,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(357,20251101,89,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(358,20250501,56,1,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(359,20251201,56,1,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(360,20250201,56,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(361,20250301,56,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(362,20250701,56,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(363,20250801,56,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(364,20250901,56,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(365,20251001,56,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(366,20251101,56,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(367,20251201,56,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(368,20250101,86,1,7,0,0,7,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(369,20250201,86,1,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(370,20250301,86,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(371,20250401,86,1,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(372,20250501,86,1,6,0,0,6,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(373,20250601,86,1,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(374,20250701,86,1,8,0,0,8,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(375,20250801,86,1,3,0,0,3,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(376,20250901,86,1,7,0,0,7,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(377,20251001,86,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(378,20251101,86,1,5,0,0,5,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(379,20251201,86,1,4,0,0,4,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(380,20250101,86,2,15,0,0,15,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(381,20250201,86,2,13,0,0,13,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(382,20250301,86,2,20,0,0,20,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(383,20250401,86,2,13,0,0,13,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(384,20250501,86,2,16,0,0,16,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(385,20250601,86,2,10,0,0,10,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(386,20250701,86,2,12,0,0,12,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(387,20250801,86,2,15,0,0,15,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(388,20250901,86,2,19,0,0,19,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(389,20251001,86,2,10,0,0,10,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(390,20251101,86,2,16,0,0,16,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(391,20251201,86,2,15,0,0,15,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(392,20250301,65,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(393,20250501,65,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(394,20250601,65,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(395,20250701,65,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(396,20250801,65,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(397,20251001,65,2,2,0,0,2,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(398,20251101,65,2,1,0,0,1,0,0);
INSERT INTO "fato_violencia_sinesp" VALUES(399,20251201,65,2,1,0,0,1,0,0);
CREATE TABLE fato_vitimas_fogo_cruzado (
        id_fato_fc          INTEGER PRIMARY KEY,
        vitima_hash_lgpd    CHAR(16) NOT NULL,
        ocorrencia_hash     CHAR(16) NOT NULL,
        id_tempo            INTEGER NOT NULL REFERENCES dim_tempo(id_tempo),
        id_localidade       INTEGER NOT NULL REFERENCES dim_localidade(id_localidade),
        id_perfil           INTEGER NOT NULL REFERENCES dim_perfil_vitima(id_perfil),
        id_contexto         INTEGER NOT NULL REFERENCES dim_contexto_crime(id_contexto),
        situacao_vitima     VARCHAR(20) NOT NULL,
        is_fatal            SMALLINT NOT NULL,
        idade_vitima        SMALLINT,
        lat_aprox           NUMERIC(6, 2),
        lon_aprox           NUMERIC(6, 2)
    );
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(1,'2f708854','97dbe5cb',20250108,9,6,3,'Morto',1,20,-12.94,-38.49);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(2,'9ddfd32f','64c8a9ad',20250112,18,6,4,'Morto',1,23,-12.92,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(3,'5e7347ae','2b611a81',20250221,25,4,5,'Morto',1,30,-12.87,-38.47);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(4,'7db8660d','2bde7bda',20250314,28,4,6,'Morto',1,28,-12.94,-38.4);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(5,'c37eb7a5','a6e0a6b4',20250315,12,4,7,'Morto',1,34,-13,-38.5);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(6,'67936ce5','cbee05af',20250408,17,5,5,'Morto',1,36,-12.93,-38.46);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(7,'24253104','3831b017',20250413,14,6,8,'Morto',1,19,-12.95,-38.46);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(8,'f4af970b','91991827',20250426,30,8,9,'Ferido',0,39,-12.97,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(9,'b6770461','286646cb',20250513,6,6,5,'Morto',1,21,-12.9,-38.44);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(10,'e0153dd6','8ffafed3',20250608,24,4,10,'Morto',1,29,-12.96,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(11,'566da126','418784c1',20250615,18,8,3,'Morto',1,35,-12.91,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(12,'13ee236e','90112882',20250628,7,9,11,'Ferido',0,21,-12.92,-38.47);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(13,'ddf20ae6','052dc678',20250701,19,4,12,'Morto',1,27,-12.93,-38.5);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(14,'9ec6adc4','0f0d1b22',20250705,15,7,13,'Ferido',0,32,-12.96,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(15,'9d16a2c8','b4f4075a',20250713,29,1,3,'Morto',1,26,-12.93,-38.42);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(16,'9146896f','b86aa70e',20250717,16,8,14,'Morto',1,40,-12.9,-38.35);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(17,'6c7e6e7f','cf9bc0dd',20250722,13,11,15,'Ferido',0,22,-12.99,-38.5);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(18,'d48cf252','3fa8a873',20250725,27,5,3,'Morto',1,44,-12.91,-38.43);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(19,'c1b3534a','66b04365',20250801,11,9,3,'Morto',1,20,-12.98,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(20,'f74ce0f0','586cc7dd',20250904,18,10,5,'Morto',1,26,-12.91,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(21,'f438c806','4ef67154',20250905,8,6,5,'Morto',1,18,-12.99,-38.49);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(22,'5e23948a','a1f8e03f',20250918,15,6,16,'Morto',1,24,-12.95,-38.48);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(23,'5310d35a','aa746abc',20250925,26,7,17,'Ferido',0,25,-12.91,-38.38);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(24,'eb60ddeb','f77ba693',20250928,21,8,18,'Ferido',0,38,-13.01,-38.47);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(25,'76360e83','e8d5f51e',20251117,23,8,13,'Ferido',0,40,-12.92,-38.45);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(26,'bb8104ad','d1e3725c',20251122,20,6,16,'Morto',1,20,-12.85,-38.45);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(27,'06f130a9','ed1702f8',20251218,10,7,3,'Ferido',0,28,-12.99,-38.52);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(28,'d7fbb5da','ba9c4dc3',20251223,8,6,19,'Morto',1,23,-12.98,-38.47);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(29,'c5f4f734','65052c6d',20250108,60,5,3,'Morto',1,40,-1.47,-48.46);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(30,'1da602fb','fa083c25',20250312,62,1,20,'Morto',1,32,-1.43,-48.47);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(31,'da834065','35b4acab',20250209,43,1,21,'Morto',1,29,-8.13,-34.95);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(32,'9c4e1bc3','e974a8e3',20250214,41,7,22,'Ferido',0,32,-8.05,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(33,'ff565c49','e974a8e3',20250214,41,8,22,'Ferido',0,37,-8.05,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(34,'b305ea93','b476a31d',20250226,47,4,21,'Morto',1,33,-7.99,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(35,'9cfca37a','abcf327d',20250309,51,5,23,'Morto',1,42,-8.05,-34.91);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(36,'09b05d69','6c3b3ad0',20250310,37,9,3,'Morto',1,19,-7.99,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(37,'896018c2','c7d4b664',20250408,53,6,3,'Morto',1,20,-8.05,-34.96);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(38,'d9f33076','274e97be',20250419,49,4,16,'Morto',1,28,-8.07,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(39,'482f4470','86120df0',20250507,42,6,21,'Morto',1,19,-8,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(40,'594dc8a5','a381e879',20250513,44,6,3,'Morto',1,22,-8.04,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(41,'532c4b98','b9f14208',20250528,47,8,3,'Ferido',0,36,-7.99,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(42,'024af572','6c6be945',20250529,39,5,5,'Morto',1,39,-8.03,-34.92);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(43,'53366793','ff88cbb8',20250617,34,7,24,'Ferido',0,29,-8.08,-34.91);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(44,'e8116bbe','b532d19a',20250705,45,5,3,'Ferido',0,36,-8.02,-34.93);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(45,'6feeec87','c16fb6af',20250705,48,6,3,'Morto',1,19,-8.01,-34.89);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(46,'c52b11b9','ab47efb4',20250810,38,4,3,'Morto',1,32,-8,-34.92);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(47,'4aec3082','638ed97d',20250814,35,4,16,'Morto',1,26,-8.02,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(48,'54adc4cb','e3daafba',20250820,52,6,3,'Morto',1,23,-8.06,-34.94);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(49,'39f0477d','96445d03',20250927,40,5,3,'Ferido',0,44,-8.12,-34.96);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(50,'64ea4994','9346aa59',20251006,50,8,3,'Morto',1,35,-8.07,-34.88);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(51,'f8b76f87','670f8292',20251012,35,9,25,'Ferido',0,18,-8.02,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(52,'f7916a53','80f45fb2',20251105,50,4,5,'Morto',1,30,-8.07,-34.89);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(53,'cd6707ff','556846ac',20251207,51,6,3,'Morto',1,19,-8.05,-34.92);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(54,'69996276','caa40a71',20251224,42,7,3,'Ferido',0,33,-8,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(55,'dd27b3c2','a01ba231',20251228,38,4,5,'Morto',1,27,-8,-34.92);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(56,'fc0ad7c0','12f662b6',20251228,36,7,3,'Ferido',0,25,-8.02,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(57,'ce670ab4','12f662b6',20251228,36,7,3,'Ferido',0,29,-8.02,-34.9);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(58,'2184f792','f4565097',20250115,84,8,26,'Ferido',0,38,-22.85,-43.49);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(59,'5eb65c44','3f1d9f4b',20250120,69,8,27,'Ferido',0,38,-22.89,-43.22);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(60,'99537340','337f0657',20250124,79,3,28,'Ferido',0,19,-22.85,-43.29);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(61,'5a9c1b2a','15b5840b',20250212,83,8,8,'Ferido',0,45,-22.81,-43.31);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(62,'8d575780','ec6ac1cd',20250303,71,8,16,'Ferido',0,40,-22.92,-43.18);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(63,'fc12c849','25f83496',20250624,85,8,29,'Ferido',0,45,-22.89,-43.36);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(64,'1444bc5e','088c4b4a',20250722,68,1,30,'Ferido',0,31,-22.89,-43.46);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(65,'8dfe954a','7bc97dd8',20250726,68,2,31,'Ferido',0,43,-22.85,-43.46);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(66,'666e6415','77585456',20250814,70,1,32,'Morto',1,28,-22.89,-43.33);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(67,'c256fccf','b577b692',20250817,74,9,21,'Morto',1,24,-22.91,-43.6);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(68,'92de501d','a59fb6fb',20250820,76,5,33,'Morto',1,36,-22.88,-43.41);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(69,'7d421ec4','be36ce40',20250905,73,9,34,'Morto',1,18,-22.96,-43.35);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(70,'28a04f44','f315ec44',20251024,72,1,35,'Ferido',0,27,-22.95,-43.38);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(71,'b1675e78','f4191866',20251104,80,3,3,'Morto',1,24,-22.97,-43.7);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(72,'e24e41b1','1d47f85b',20251114,81,4,36,'Ferido',0,31,-22.8,-43.18);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(73,'699980b9','1d47f85b',20251114,81,9,37,'Ferido',0,23,-22.8,-43.18);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(74,'5b401573','20291fbd',20251123,82,1,38,'Ferido',0,28,-22.93,-43.24);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(75,'e5b87b3c','352d6f44',20251128,77,2,39,'Morto',1,41,-22.91,-43.22);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(76,'484ceae3','352d6f44',20251128,77,2,39,'Morto',1,40,-22.91,-43.22);
INSERT INTO "fato_vitimas_fogo_cruzado" VALUES(77,'0ae825bb','4b25fe4e',20251220,75,6,35,'Morto',1,21,-22.85,-43.32);
CREATE INDEX idx_dim_tempo_ano_mes ON dim_tempo (ano, mes);
CREATE INDEX idx_dim_localidade_regiao_uf ON dim_localidade (regiao, uf);
CREATE INDEX idx_dim_localidade_municipio ON dim_localidade (municipio);
CREATE INDEX idx_dim_perfil_interseccional ON dim_perfil_vitima (macro_genero, raca_cor, grupo_interseccional);
CREATE INDEX idx_dim_contexto_evento ON dim_contexto_crime (fonte_dados, tipo_evento);
CREATE INDEX idx_fato_sinesp_tempo_loc ON fato_violencia_sinesp (id_tempo, id_localidade);
CREATE INDEX idx_fato_sinesp_contexto ON fato_violencia_sinesp (id_contexto);
CREATE INDEX idx_fato_fc_tempo_loc ON fato_vitimas_fogo_cruzado (id_tempo, id_localidade);
CREATE INDEX idx_fato_fc_perfil ON fato_vitimas_fogo_cruzado (id_perfil);
CREATE INDEX idx_fato_fc_contexto ON fato_vitimas_fogo_cruzado (id_contexto);
CREATE VIEW vw_resumo_interseccional_fogo_cruzado AS
    SELECT
        t.ano,
        t.mes,
        t.nome_mes,
        t.trimestre,
        l.regiao,
        l.uf,
        l.estado,
        l.municipio,
        l.bairro,
        p.genero,
        p.macro_genero,
        p.raca_cor,
        p.faixa_etaria,
        p.tipo_pessoa,
        p.grupo_interseccional,
        c.tipo_evento AS motivo_principal,
        c.acao_policial,
        c.presenca_agente,
        c.chacina,
        c.circunstancia,
        c.local_ocorrencia,
        f.situacao_vitima,
        f.is_fatal,
        f.idade_vitima,
        f.lat_aprox,
        f.lon_aprox
    FROM fato_vitimas_fogo_cruzado f
    JOIN dim_tempo t          ON f.id_tempo = t.id_tempo
    JOIN dim_localidade l     ON f.id_localidade = l.id_localidade
    JOIN dim_perfil_vitima p  ON f.id_perfil = p.id_perfil
    JOIN dim_contexto_crime c ON f.id_contexto = c.id_contexto;
CREATE VIEW vw_resumo_violencia_sinesp AS
    SELECT
        t.ano,
        t.mes,
        t.nome_mes,
        t.trimestre,
        l.regiao,
        l.uf,
        l.estado,
        l.municipio,
        c.tipo_evento,
        c.arma,
        c.agente_seguranca,
        f.vitimas_feminino,
        f.vitimas_masculino,
        f.vitimas_nao_inf,
        f.total_vitimas,
        f.total_ocorrencias,
        f.total_peso
    FROM fato_violencia_sinesp f
    JOIN dim_tempo t          ON f.id_tempo = t.id_tempo
    JOIN dim_localidade l     ON f.id_localidade = l.id_localidade
    JOIN dim_contexto_crime c ON f.id_contexto = c.id_contexto;
COMMIT;
