function transform(line) {
    const parameters = [];
    let withinQuotes = false;
    let currentParameter = "";

    for (let i = 0; i < line.length; i++) {
        const character = line[i];
        if (character === "\"") {
            withinQuotes = !withinQuotes;
        } else if (character === "," && !withinQuotes) {
            parameters.push(currentParameter.trim());
            currentParameter = "";
        } else {
            currentParameter += character;
        }
    }

    // Check if there's a parameter still being built
    parameters.push(currentParameter.trim());

    // Check for unclosed quotes
    if (withinQuotes) {
        console.log("ERROR: Quote left open");
        return null;
    }

    var obj = new Object();
    obj.id = parameters[0];
    obj.type = parameters[1];
    obj.bowling = parameters[2];
    obj.batting =parameters[3];
  
    const jsonData = JSON.stringify(obj);
    
    

    return jsonData;
}


// Example usage:

 // Output: ['param1', 'quoted param 2', 'param3']
