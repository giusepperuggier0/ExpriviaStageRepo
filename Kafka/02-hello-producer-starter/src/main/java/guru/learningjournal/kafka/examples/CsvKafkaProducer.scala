package guru.learningjournal.kafka.examples

import java.util.Properties
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import com.github.tototoshi.csv._
import java.io.File

object CsvKafkaProducer {
  def main(args: Array[String]): Unit = {
    val broker = "localhost:9092"  // Indirizzo del broker Kafka
    val topic = "csv_topic"         // Nome del topic Kafka
    val csvFile = "dati.csv"        // Percorso del file CSV
    val delimiter = ','             // Delimitatore CSV

    val props = new Properties()
    props.put("bootstrap.servers", broker)
    props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
    props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")

    val producer = new KafkaProducer[String, String](props)
    val reader = CSVReader.open(new File(csvFile))(new DefaultCSVFormat {
      override val delimiter = delimiter
    })

    val headers = reader.readNext().getOrElse(Seq())
    reader.foreach { row =>
      val dataMap = headers.zip(row).toMap
      val message = dataMap.map { case (k, v) => s"$k: $v" }.mkString(", ")
      val record = new ProducerRecord[String, String](topic, message)
      producer.send(record)
      println(s"Inviato: $message")
    }

    reader.close()
    producer.close()
  }
}
