// 1. Get the tweet text using prompt() directly
var tweet = prompt("what is your tweet ");

// 2. Get the length of that text
var tweeting_score = tweet.length;

if (tweeting_score > 150) {
    // 3. Subtract 150 from the LENGTH (tweeting_score), not the text
    alert("you have gone " + (tweeting_score - 150) + " over the 150 character limit ");
} 
else {
    alert("your tweet " + tweet + " has been tweeted ");
}