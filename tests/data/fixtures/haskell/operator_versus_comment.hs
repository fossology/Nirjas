module Demo where

-- a genuine line comment
(-->) :: Int -> Int -> Int
x --> y = x + y           -- the operator above is user-defined, not comment syntax

notAComment :: String
notAComment = "-- not a comment"

{- outer {- nested block -} still outer -}
main :: IO ()
main = putStrLn notAComment -- trailing comment after code
