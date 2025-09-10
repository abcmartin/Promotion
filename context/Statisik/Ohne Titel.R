source("~/dissertation /diss2/untitled.R")
# Bibliotheken laden
library(survival)
library(ggplot2)
library(dplyr)

# Daten einlesen
daten <- read.csv("Dissertation_Daten.csv")

# a. Deskriptive Analyse
# Verteilung von Patientenmerkmalen
ggplot(daten, aes(x=Alter)) + geom_histogram(binwidth=5) + ggtitle("Verteilung des Alters")

# Verteilung von Tumorcharakteristiken
ggplot(daten, aes(x=TumorStadium)) + geom_histogram(binwidth=1) + ggtitle("Verteilung des Tumor-Stadiums")

# Verteilung von Behandlungsmerkmalen
ggplot(daten, aes(x=Behandlungsart)) + geom_bar() + ggtitle("Verteilung der Behandlungsarten")

# b. Ereigniszeitanalysen
# Loko-regionale Tumorkontrolle
fit_loko <- survfit(Surv(Zeit, LokoRegionaleKontrolle) ~ CD44_Expression + HPV16_DNA_Status, data=daten)
plot(fit_loko, main="Loko-regionale Tumorkontrolle")

# Fernmetastasen-freies Überleben
fit_fern <- survfit(Surv(Zeit, FernMetastasenFrei) ~ CD44_Expression + HPV16_DNA_Status, data=daten)
plot(fit_fern, main="Fernmetastasen-freies Überleben")

# Gesamtüberleben
fit_gesamt <- survfit(Surv(Zeit, GesamtUeberleben) ~ CD44_Expression + HPV16_DNA_Status, data=daten)
plot(fit_gesamt, main="Gesamtüberleben")

# c. Multivariate Analysen
# Cox Proportional Hazards Modell
fit_cox <- coxph(Surv(Zeit, GesamtUeberleben) ~ CD44_Expression + HPV16_DNA_Status + Alter + Geschlecht + TumorStadium, data=daten)
summary(fit_cox)

