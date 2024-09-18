// src/tweetnacl.d.ts

import 'tweetnacl';

declare module 'tweetnacl' {
  namespace box {
    interface BoxKeyPair {
      publicKey: Uint8Array;
      secretKey: Uint8Array;
    }

    function keyPairFromSeed(seed: Uint8Array): BoxKeyPair;
  }
}
