const express = require('express');
const path = require('path');
const app = express();
const port = 7000;

// Serve static files from the 'build' directory
app.use(express.static(path.join(__dirname, 'build')));

// Define a catch-all route to serve your React app
app.get('/:source', (req, res) => {
    if (!req.params.source) {
        res.sendFile(path.join(__dirname, 'build', 'index.html'));
        return
    }
    try {
        if (path.join(__dirname, 'build', req.params.source)) {
            res.sendFile(path.join(__dirname, 'build', req.params.source));
        } else {
            res.sendFile(path.join(__dirname, 'build', 'not_found.html'));
        }
    } catch (error) {
        console.log(error);
    }
    // if (path.join(__dirname, 'build', req.params.source)) {
    //     res.sendFile(path.join(__dirname, 'build', req.params.source));
    // } else {
    //     res.sendFile(path.join(__dirname, 'build', "not_found.html"));
    // }

});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
