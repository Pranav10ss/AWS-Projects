exports.handler = async (event) => {
    console.log(JSON.stringify(event));
    for (const record of event.Records) {
        const data = JSON.parse(Buffer.from(record.kinesis.data, 'base64'));
        //send emails to clients, publish stuff to social media
        console.log('consumer #2', data);
    }
};
