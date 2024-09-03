const axios = require("axios");
const cheerio = require("cheerio");
const fs = require("fs");

function cleanText(content) {
  return content
    .replace(/<script.*?>.*?<\/script>/gis, "") // Remove script tags
    .replace(/<\/?[^>]+(>|$)/g, "") // Remove HTML tags
    .replace(/\s+/g, " ") // Replace multiple spaces, newlines, tabs with a single space
    .trim() // Trim leading and trailing whitespace
    .replace(/※.*※/g, "");
}

function getCurrentDateString() {
  const date = new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Months are 0-indexed, so we add 1
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
}

function getDomainName(url) {
  const { hostname } = new URL(url);
  return hostname;
}

function getTitle($) {
  return $("title").text() || "No title";
}

function getDescription($) {
  return $('meta[name="description"]').attr("content") || "No description";
}

function getContent($) {
  return (
    $(".article_content").text() ||
    $(".subject_article p")
      .map((i, el) => $(el).text().trim())
      .get()
      .join("\n") ||
    "No content available"
  );
}

function getDate($) {
  return (
    $('time.date[itemprop="datePublished"]').text().trim() || // Extract datetime attribute
    $("time.date").text().trim() || // Extract the text content if datetime is not available
    $("div.article_date").text() ||
    $('meta[property="article:published_time"]').attr("content") ||
    "No date"
  );
}

function getKeywords($) {
  return (
    $('meta[name="keywords"]').attr("content") ||
    $('meta[name="news_keywords"]').attr("content") ||
    "No keywords"
  );
}

function normalizeUrl(url) {
  try {
    const parsedUrl = new URL(url);
    // Remove query parameters and fragments
    parsedUrl.search = "";
    parsedUrl.hash = "";
    return parsedUrl.toString();
  } catch (err) {
    console.error(`Invalid URL: ${url}`);
    return null;
  }
}

const bfsWebCrawler = async (options = {}) => {
  const startUrl = options.queue[0];
  const visitedUrls = new Set();
  const queue = [...options.queue];
  const results = [];

  const maxDepth = options.maxDepth || 3;
  const maxPages = options.maxPages || 50;
  const userAgent =
    options.userAgent ||
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)";
  const delay = options.delay || 0;
  const targetPaths = options.targetPaths || [];

  let currentDepth = 0;

  const crawl = async (url) => {
    if (visitedUrls.has(url) || results.length >= maxPages) return;

    try {
      const response = await axios.get(url, {
        headers: { "User-Agent": userAgent },
        timeout: options.timeout || 10000,
      });

      const $ = cheerio.load(response.data);
      const title = getTitle($);
      const description = getDescription($);
      const date = getDate($);
      const content = cleanText(getContent($));
      const keywords = getKeywords($);

      console.log({
        url,
        title,
        description,
        date,
        content,
        keywords,
      });

      if (content !== "No content available") {
        results.push({
          url,
          title,
          description,
          date,
          content,
          keywords,
        });
      }

      visitedUrls.add(url);

      // Enqueue links for BFS, but only if they are within the same domain
      $("a[href]").each((_, element) => {
        let link = $(element).attr("href");

        // Convert relative URLs to absolute URLs
        if (!link.startsWith("http")) {
          link = new URL(link, startUrl).href;
        }

        const normalizedLink = normalizeUrl(link);
        if (!normalizedLink) return;

        const linkPath = new URL(normalizedLink).pathname;
        const isSameDomain = normalizedLink.includes(options.matchDomain);

        // Check if the linkPath matches any of the targetPaths
        const matchesTargetPath = targetPaths.some((path) =>
          linkPath.startsWith(path)
        );

        if (
          isSameDomain &&
          matchesTargetPath &&
          !visitedUrls.has(normalizedLink) &&
          currentDepth < maxDepth
        ) {
          queue.push(normalizedLink);
        }
      });

      console.log("Queue length:", queue.length);
      currentDepth++;
    } catch (error) {
      console.error(`Failed to fetch ${url}:`, error.message);
    }
  };

  while (queue.length > 0 && results.length < maxPages) {
    const nextUrl = queue.shift();
    await crawl(nextUrl);
    console.log("URL Done:", nextUrl);

    // Implement delay to avoid rate-limiting issues
    if (delay > 0) {
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  // Save results to JSON file
  const fileName = `${getDomainName(startUrl)}_${getCurrentDateString()}.json`;
  fs.writeFileSync(fileName, JSON.stringify(results, null, 2), "utf-8");

  console.log(`Crawling completed. Results saved to ${fileName}`);
};

function run() {
  const options = {
    maxDepth: 10,
    maxPages: 1000,
    timeout: 8000,
    matchDomain: "ettoday",
    queue: [
      "https://finance.ettoday.net/",
      "https://forum.ettoday.net/",
      "https://www.ettoday.net/news/focus/%E5%9C%8B%E9%9A%9B/",
      "https://www.ettoday.net/news/focus/%E5%A4%A7%E9%99%B8/",
      "https://www.ettoday.net/news/hot-news.htm",
    ],
    targetPaths: ["/news/"],
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", // Custom user-agent
    delay: 2000,
  };

  bfsWebCrawler(options);

  const options2 = {
    maxDepth: 10,
    maxPages: 1000,
    timeout: 8000,
    matchDomain: "news.ebc.net",
    queue: [
      "https://news.ebc.net.tw/news/business",
      "https://news.ebc.net.tw/news/world",
    ],
    targetPaths: ["/news/world", "/news/business"],
    userAgent:
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", // Custom user-agent
    delay: 2000,
  };

  bfsWebCrawler(options2);
}

run();
