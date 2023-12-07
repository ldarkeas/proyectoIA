const toxicity = require('@tensorflow-models/toxicity');
const threshold = 0.8;

const classify = async (model, text) => {
    const sentences = [text]
    let predictions = await model.classify(sentences);
    predictions = predictions.map(prediction => ({
        label: prediction["label"],
        match: prediction.results[0]["match"]
    }))

    return predictions.filter(p => p.match).map(p => p.label)
}

const main = async (text) => {
    const model = await toxicity.load(threshold)
    const predictions = await classify(model, text)
    if (predictions.length == 0) {
        process.stdout.write("Probablemente no es un comentario toxico y sea apropiado para menores.")
    }
    else {
        process.stdout.write(JSON.stringify(predictions+" No es apropiado para menores"))
    }
}

main(process.argv[2]);