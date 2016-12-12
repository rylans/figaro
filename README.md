# figaro [![Build Status](https://travis-ci.org/rylans/figaro.svg?branch=master)](https://travis-ci.org/rylans/figaro)
CLI personal assistant 

### Install

Git-clone and then pip install:

```
> pip install .
```

### API Usage

```
>>> from figaro import Figaro
>>> figaro = Figaro()
>>> figaro.hears("What is the square root of 16")
'4.0'
>>> figaro.hears("My name is Lisa")
'Nice to meet you.'
>>> figaro.hears("Bye")
'See you later!'

```

### License

- Licensed under the Apache License, Version 2.0 (the "License");
- you may not use this software except in compliance with the License.
- You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
