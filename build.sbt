name := "VulnerableScalaApp"

version := "0.1"

scalaVersion := "2.11.8" // Old version, multiple vulnerabilities

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "2.1.0",            // CVE-2018-17190 - Arbitrary code execution via Java deserialization
  "org.scala-lang.modules" %% "scala-xml" % "1.0.2",        // CVE-2017-18640 - XXE vulnerability
  "com.typesafe.akka" %% "akka-http" % "10.0.0",            // CVE-2018-16115 - Header injection
  "com.fasterxml.jackson.core" % "jackson-databind" % "2.9.5", // Multiple CVEs incl. RCE via polymorphic type handling
  "org.apache.commons" % "commons-collections4" % "4.0",    // CVE-2015-6420 - Deserialization RCE
  "commons-beanutils" % "commons-beanutils" % "1.9.2",      // CVE-2019-10086 - Deserialization vulnerability
  "org.bouncycastle" % "bcprov-jdk15on" % "1.55",           // CVE-2016-1000341 - Crypto vulnerability
  "org.jsoup" % "jsoup" % "1.8.3",                          // CVE-2021-37714 - XSS due to improper sanitization
  "org.apache.struts" % "struts2-core" % "2.3.24",          // CVE-2017-5638 - RCE via crafted Content-Type
  "org.slf4j" % "slf4j-api" % "1.7.12"                      // CVE-2017-18318 - Deserialization issue in logging
)
