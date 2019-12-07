-- Table: "B03_Coffee"."Samples"

-- DROP TABLE "B03_Coffee"."Samples";

CREATE TABLE "B03_Coffee"."Samples"
(
    "Sample_ID" integer NOT NULL,
    "Sample_ImagePath" "char"[] NOT NULL,
    "Sample_data" jsonb NOT NULL,
    "Sample_CreateDate" date NOT NULL,
    CONSTRAINT "Samples_pkey" PRIMARY KEY ("Sample_ID")
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE "B03_Coffee"."Samples"
    OWNER to postgres;