name := "TestScalaApplication"

version := "0.1"

scalaVersion := "2.13.8"

// Add dependencies with known vulnerabilities
libraryDependencies ++= Seq(
  "com.typesafe.akka" %% "akka-actor" % "2.5.31",  // Example of potential vulnerabilities
  "org.apache.logging.log4j" % "log4j-core" % "2.14.1"  // Critical vulnerabilities might exist
)