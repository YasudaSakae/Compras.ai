Exception in thread "main" com.google.gson.JsonSyntaxException: com.google.gson.stream.MalformedJsonException: Use JsonReader.setLenient(true) to accept malformed JSON at line 1 column 6 path $
        at com.google.gson.JsonParser.parseReader(JsonParser.java:66)
        at com.google.gson.JsonParser.parseString(JsonParser.java:47)
        at br.com.sinerji.comprascrawler.crawler.pncp.PNCPSearchHiresCrawler.getResultJsonObject(PNCPSearchHiresCrawler.java:144)
        at br.com.sinerji.comprascrawler.crawler.pncp.PNCPSearchHiresCrawler.fetchPages(PNCPSearchHiresCrawler.java:81)
        at br.com.sinerji.comprascrawler.crawler.pncp.PNCPSearchHiresCrawler.runCrawler(PNCPSearchHiresCrawler.java:58)
        at br.com.sinerji.comprascrawler.crawler.Crawler.execute(Crawler.java:23)
        at br.com.sinerji.comprascrawler.crawler.CrawlersExecutor.execute(CrawlersExecutor.java:65)
        at br.com.sinerji.comprascrawler.Main.executeCrawlers(Main.java:42)
        at br.com.sinerji.comprascrawler.Main.main(Main.java:27)
Caused by: com.google.gson.stream.MalformedJsonException: Use JsonReader.setLenient(true) to accept malformed JSON at line 1 column 6 path $
        at com.google.gson.stream.JsonReader.syntaxError(JsonReader.java:1597)
        at com.google.gson.stream.JsonReader.checkLenient(JsonReader.java:1404)
        at com.google.gson.stream.JsonReader.doPeek(JsonReader.java:542)
        at com.google.gson.stream.JsonReader.peek(JsonReader.java:425)
        at com.google.gson.JsonParser.parseReader(JsonParser.java:61)
        ... 8 more

mvn package clean
java -jar target/compras-crawler.jar


Get-ChildItem -Path "C:\caminho\da\pasta" -Filter "*.pdf" | Measure-Object | Select-Object -ExpandProperty Count


Erro na leitura de D:\ARQUIVOS\EDITAIS-BRUTO\PDF\00059311000126-193-2022.pdf: EOF marker not found
Operação 'erro_leitura': 0.127s
Traceback (most recent call last):
  File "d:\SISTEMAS\SCRIPTS\pdf-classifier.py", line 186, in <module>
    process_pdfs(input_path)
  File "d:\SISTEMAS\SCRIPTS\pdf-classifier.py", line 154, in process_pdfs
    title, content, success = extract_text_from_pdf(pdf_path, timer)
    ^^^^^^^^^^^^^^^^^^^^^^^
ValueError: not enough values to unpack (expected 3, got 2)
