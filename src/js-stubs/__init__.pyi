from collections.abc import (
  Callable,
  Iterable as PyIterable,
  Iterator as PyIterator,
  AsyncIterator as PyAsyncIterator,
  AsyncIterable as PyAsyncIterable,
  Generator as PyGenerator,
  MutableSequence as PyMutableSequence,
  Sequence as PySequence,
  Awaitable,
)
from asyncio import Future
from typing import (
  overload,
  Any,
  Literal,
  Self,
  ClassVar,
  Never,
  Protocol,
)

from pyodide.ffi import (
  JsProxy,
  JsIterable,
  JsGenerator,
  JsIterator,
  JsAsyncIterator,
  JsArray,
  JsMutableMap,
  JsMap as ReadonlyMap,
  JsBuffer,
)
from pyodide.webloop import PyodideFuture
from _pyodide._core_docs import _JsProxyMetaClass

type ConcatArray[T] = JsArray[T]
type ArrayLike[T] = JsArray[T]
type ArrayLike_iface[T] = PyMutableSequence[T]
type Iterable_iface[T] = PyIterable[T]

class Thenable[T](Protocol):
  def then[TResult1, TResult2](
      self,
      onfulfilled: (Callable[[T], TResult1 | PromiseLike_iface[TResult1]])
      | None
      | None = None,
      onrejected: (Callable[[Any], TResult2 | PromiseLike_iface[TResult2]])
      | None = None,
      /,
  ) -> PromiseLike_iface[TResult1 | TResult2]:
      ...

type PromiseLike_iface[T] = Awaitable[T] | Thenable[T]


type Dispatcher = Any
type URL_ = URL
type HeadersInit = PyIterable[tuple[str, str]] | Record[str, str] | Headers

# Shenanigans to convince skeptical type system to behave correctly:
#
# These classes we are declaring are actually JavaScript objects, so the class
# objects themselves need to be instances of JsProxy. So their type needs to
# subclass JsProxy. We do this with a custom metaclass.


class Promise[T](PyodideFuture[T]):
  @classmethod
  def new(
      cls,
      executor: Callable[[], None]
      | Callable[[Callable[[T], None]], None]
      | Callable[[Callable[[T], None], Callable[[BaseException], None]], None],
  ) -> Promise[T]:
    ...


class Map[KT, VT](JsMutableMap[KT, VT]):
  @classmethod
  @overload
  def new(cls) -> "JsMutableMap[KT, VT]":
    ...

  @classmethod
  @overload
  def new(cls, args: PySequence[tuple[KT, VT]]) -> "JsMutableMap[KT, VT]":
    ...


class _JsMeta(_JsProxyMetaClass, JsProxy):
  pass


class DoNotCallThis:
  pass


class _JsObject(metaclass=_JsMeta):
  def __new__(self, do_not_call: DoNotCallThis) -> _JsObject:
    ...


class Record[S, T](JsProxy):
  def __getattr__(self, s: str) -> T:
    ...


type CfProperties[HostMetadata=Any] = IncomingRequestCfProperties[HostMetadata] | RequestInitCfProperties_iface

type RequestInfo[CfHostMetadata=Any, Cf=Any] = Request[CfHostMetadata, Cf] | str

type BodyInit = ReadableStream[Uint8Array[ArrayBufferLike]] | str | ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike] | Blob | URLSearchParams | FormData | JsIterable[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]] | JsAsyncIterable[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]]

type ArrayBufferLike = Any

type PropertyKey = str | int | float | Symbol

type Awaited[T] = Any

type EventListenerOrEventListenerObject[EventType=Event] = EventListener[EventType] | EventListenerObject_iface[EventType]

type DurableObjectLocationHint = Literal["wnam", "enam", "sam", "weur", "eeur", "apac", "oc", "afr", "me"]

type DurableObjectJurisdiction = Literal["eu", "fedramp", "fedramp-high"]

type R2Range = R2Range__Union0 | R2Range__Union1 | R2Range__Union2

type ReadableStreamReadResult[R=Any] = ReadableStreamReadResult__Union0[R] | ReadableStreamReadResult__Union1

type AiImageClassificationOutput = JsArray[AiImageClassificationOutput__array]

type AiObjectDetectionOutput = JsArray[AiObjectDetectionOutput__array]

type AiSentenceSimilarityOutput = JsArray[int | float]

type AiTextClassificationOutput = JsArray[AiTextClassificationOutput__array]

type AiTextToSpeechOutput = Uint8Array[ArrayBufferLike] | AiTextToSpeechOutput__Union1

type AiTextToImageOutput = ReadableStream[Uint8Array[ArrayBufferLike]]

type Ai_Cf_Baai_Bge_Base_En_V1_5_Input = Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union0 | Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union1

type Ai_Cf_Baai_Bge_Base_En_V1_5_Output = Ai_Cf_Baai_Bge_Base_En_V1_5_Output__Union0 | Ai_Cf_Baai_Bge_Base_En_V1_5_AsyncResponse_iface

type Ai_Cf_Openai_Whisper_Input = str | Ai_Cf_Openai_Whisper_Input__Union1

type Ai_Cf_Meta_M2M100_1_2B_Input = Ai_Cf_Meta_M2M100_1_2B_Input__Union0 | Ai_Cf_Meta_M2M100_1_2B_Input__Union1

type Ai_Cf_Meta_M2M100_1_2B_Output = Ai_Cf_Meta_M2M100_1_2B_Output__Union0 | Ai_Cf_Meta_M2M100_1_2B_AsyncResponse_iface

type Ai_Cf_Baai_Bge_Small_En_V1_5_Input = Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union0 | Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union1

type Ai_Cf_Baai_Bge_Small_En_V1_5_Output = Ai_Cf_Baai_Bge_Small_En_V1_5_Output__Union0 | Ai_Cf_Baai_Bge_Small_En_V1_5_AsyncResponse_iface

type Ai_Cf_Baai_Bge_Large_En_V1_5_Input = Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union0 | Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union1

type Ai_Cf_Baai_Bge_Large_En_V1_5_Output = Ai_Cf_Baai_Bge_Large_En_V1_5_Output__Union0 | Ai_Cf_Baai_Bge_Large_En_V1_5_AsyncResponse_iface

type Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input = str | Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input__Union1

type Ai_Cf_Openai_Whisper_Tiny_En_Input = str | Ai_Cf_Openai_Whisper_Tiny_En_Input__Union1

type Ai_Cf_Baai_Bge_M3_Input = Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_iface | Ai_Cf_Baai_Bge_M3_Input_Embedding_iface | Ai_Cf_Baai_Bge_M3_Input__Union2

type Ai_Cf_Baai_Bge_M3_Output = Ai_Cf_Baai_Bge_M3_Ouput_Query_iface | Ai_Cf_Baai_Bge_M3_Output_EmbeddingFor_Contexts_iface | Ai_Cf_Baai_Bge_M3_Ouput_Embedding_iface | Ai_Cf_Baai_Bge_M3_AsyncResponse_iface

type Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Input = Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Prompt_iface | Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface

type Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Input = Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Prompt_iface | Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface | Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Async_Batch_iface

type Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output = Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0 | str | Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_AsyncResponse_iface

type Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Input = Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Prompt_iface | Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface

type Ai_Cf_Qwen_Qwq_32B_Input = Ai_Cf_Qwen_Qwq_32B_Prompt_iface | Ai_Cf_Qwen_Qwq_32B_Messages_iface

type Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Input = Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Prompt_iface | Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface

type Ai_Cf_Google_Gemma_3_12B_It_Input = Ai_Cf_Google_Gemma_3_12B_It_Prompt_iface | Ai_Cf_Google_Gemma_3_12B_It_Messages_iface

type Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Input = Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Prompt_iface | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Async_Batch_iface

type Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Input = Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Prompt_iface | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Async_Batch_iface

type Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Output = Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface | str | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_AsyncResponse_iface

type Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input = Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union0 | Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union1

type Ai_Cf_Leonardo_Phoenix_1_0_Output = str

type Ai_Cf_Deepgram_Aura_1_Output = str

type Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Input = Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Prompt_iface | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Async_Batch_iface

type Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Output = Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface | str | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_AsyncResponse_iface

type Ai_Cf_Deepgram_Aura_2_En_Output = str

type Ai_Cf_Deepgram_Aura_2_Es_Output = str

type ConversionResponse = ConversionResponse__Union0 | ConversionResponse__Union1

type AIGatewayProviders = Literal['workers-ai', 'anthropic', 'aws-bedrock', 'azure-openai', 'google-vertex-ai', 'huggingface', 'openai', 'perplexity-ai', 'replicate', 'groq', 'cohere', 'google-ai-studio', 'mistral', 'grok', 'openrouter', 'deepseek', 'cerebras', 'cartesia', 'elevenlabs', 'adobe-firefly']

type AutoRagListResponse = JsArray[AutoRagListResponse__array]

type D1SessionBookmark = str

type D1SessionConstraint = Literal['first-primary', 'first-unconstrained']

type VectorFloatArray = Float32Array[ArrayBufferLike] | Float64Array[ArrayBufferLike]

type VectorizeMetadataRetrievalLevel = Literal["all", "indexed", "none"]

type WorkflowRetentionDuration = WorkflowSleepDuration

type WeakKey = Any

type EventListener[EventType=Event] = Callable[[EventType], None]

type ResponseIncludable = Literal["message.input_image.image_url", "message.output_text.logprobs"]

type ResponseInput = ArrayLike_iface[ResponseInputItem]

type ToolChoiceOptions = Literal["none"]

type Tool = ResponsesFunctionTool

type ResponseInputItem = EasyInputMessage | ResponseInputItemMessage | ResponseOutputMessage | ResponseFunctionToolCall | ResponseInputItemFunctionCallOutput | ResponseReasoningItem

type ResponseOutputItem = ResponseOutputMessage | ResponseFunctionToolCall | ResponseReasoningItem

type ResponseStatus = Literal["completed", "failed", "in_progress", "cancelled", "queued", "incomplete"]

type VectorizeIndexConfig = VectorizeIndexConfig__Union0 | VectorizeIndexConfig__Union1

type VectorizeVectorMetadata = VectorizeVectorMetadataValue | Record[str, VectorizeVectorMetadataValue]

type WorkflowSleepDuration = str | int | float

type BuiltinIteratorReturn = Any

type ReasoningEffort = Literal["minimal", "low", "medium", "high"] | None

type ResponseFormatTextConfig = ResponseFormatText | ResponseFormatTextJSONSchemaConfig | ResponseFormatJSONObject

type VectorizeDistanceMetric = Literal["euclidean", "cosine", "dot-product"]

type VectorizeVectorMetadataValue = str | int | float | bool | JsArray[str]

type IncomingRequestCfPropertiesEdgeRequestKeepAliveStatus = Literal[0, 1, 2, 3, 4, 5]

type Iso3166Alpha2Code = Literal["AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK", "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"]

type ContinentCode = Literal["AF", "AN", "AS", "EU", "NA", "OC", "SA"]

type FlatArray[Arr, Depth] = Any

type ResponseInputMessageContentList = ArrayLike_iface[ResponseInputContent]

type ResponseFunctionCallOutputItemList = ArrayLike_iface[ResponseFunctionCallOutputItem]

type CertVerificationStatus = Literal["SUCCESS", "NONE", "FAILED:self signed certificate", "FAILED:unable to verify the first certificate", "FAILED:certificate is not yet valid", "FAILED:certificate has expired", "FAILED"]

type Exclude[T, U] = Any

type ResponseInputContent = ResponseInputText | ResponseInputImage

type ResponseFunctionCallOutputItem = ResponseInputTextContent | ResponseInputImageContent

onmessage: Never = ... # type:ignore[assignment,unused-ignore]

crypto: Crypto = ... # type:ignore[assignment,unused-ignore]

caches: CacheStorage = ... # type:ignore[assignment,unused-ignore]

performance: Performance = ... # type:ignore[assignment,unused-ignore]

origin: str = ... # type:ignore[assignment,unused-ignore]

navigator: Navigator = ... # type:ignore[assignment,unused-ignore]

NaN: int | float = ... # type:ignore[assignment,unused-ignore]

Infinity: int | float = ... # type:ignore[assignment,unused-ignore]





def dispatchEvent(event: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def btoa(data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def atob(data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def setTimeout(callback: setTimeout__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def setTimeout[*Args](callback: setTimeout__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def clearTimeout(timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def setInterval(callback: setInterval__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def setInterval[*Args](callback: setInterval__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def clearInterval(timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def queueMicrotask(task: Callable[..., Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def structuredClone[T](value: T, options: StructuredSerializeOptions_iface | None = None, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def structuredClone[T](value: T, /, *, transfer: PyMutableSequence[Any] | None = None) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def reportError(error: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def fetch(input: RequestInfo[Any, CfProperties[Any]] | URL_, init: RequestInit_iface[RequestInitCfProperties_iface] | None = None, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

@overload
def fetch(input: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: RequestInitCfProperties_iface | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def eval(x: str, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def parseInt(string: str, radix: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def parseFloat(string: str, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def isNaN(number: int | float, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def isFinite(number: int | float, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def decodeURI(encodedURI: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def decodeURIComponent(encodedURIComponent: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def encodeURI(uri: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def encodeURIComponent(uriComponent: str | int | float | bool, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def escape(string: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

def unescape(string: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Env(Protocol): # type:ignore[misc, unused-ignore]
    DB: D1Database = ... # type:ignore[assignment,unused-ignore]

class ExecutionContext[Props=Any](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def exports(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def props(self, /) -> Props: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def waitUntil(self, promise: Future[Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def passThroughOnException(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectState[Props=Any](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def exports(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def props(self, /) -> Props: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def id(self, /) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def storage(self, /) -> DurableObjectStorage_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    container: Container_iface | None = ... # type:ignore[assignment,unused-ignore]
    def waitUntil(self, promise: Future[Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def blockConcurrencyWhile[T](self, callback: Callable[[], Future[T]], /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def acceptWebSocket(self, ws: WebSocket, tags: PyMutableSequence[str] | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getWebSockets(self, tag: str | None = None, /) -> JsArray[WebSocket]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setWebSocketAutoResponse(self, maybeReqResp: WebSocketRequestResponsePair | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getWebSocketAutoResponse(self, /) -> WebSocketRequestResponsePair | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getWebSocketAutoResponseTimestamp(self, ws: WebSocket, /) -> Date | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setHibernatableWebSocketEventTimeout(self, timeoutMs: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getHibernatableWebSocketEventTimeout(self, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getTags(self, ws: WebSocket, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def abort(self, reason: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class console(_JsObject): # type:ignore[misc, unused-ignore]
    
    @classmethod
    def clear(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def count(self, label: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def countReset(self, label: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def debug(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def dir(self, item: Any | None = None, options: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def dirxml(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def error(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def group(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def groupCollapsed(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def groupEnd(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def info(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def log(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def table(self, tabularData: Any | None = None, properties: PyMutableSequence[str] | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def time(self, label: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def timeEnd(self, label: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def timeLog(self, label: str | None = None, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def timeStamp(self, label: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def trace(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def warn(self, /, *data: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class self(_JsObject): # type:ignore[misc, unused-ignore]
    DOMException: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WorkerGlobalScope: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    self: ClassVar[ServiceWorkerGlobalScope_iface] = ... # type:ignore[assignment,unused-ignore]
    crypto: ClassVar[Crypto] = ... # type:ignore[assignment,unused-ignore]
    caches: ClassVar[CacheStorage] = ... # type:ignore[assignment,unused-ignore]
    scheduler: ClassVar[Scheduler_iface] = ... # type:ignore[assignment,unused-ignore]
    performance: ClassVar[Performance] = ... # type:ignore[assignment,unused-ignore]
    Cloudflare: ClassVar[Cloudflare] = ... # type:ignore[assignment,unused-ignore]
    origin: ClassVar[str] = ... # type:ignore[assignment,unused-ignore]
    Event: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ExtendableEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CustomEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    PromiseRejectionEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    FetchEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TailEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TraceEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ScheduledEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    MessageEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CloseEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamDefaultReader: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamBYOBReader: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WritableStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WritableStreamDefaultWriter: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TransformStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ByteLengthQueuingStrategy: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CountQueuingStrategy: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ErrorEvent: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    MessageChannel: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    MessagePort: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    EventSource: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamBYOBRequest: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamDefaultController: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    ReadableByteStreamController: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WritableStreamDefaultController: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TransformStreamDefaultController: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CompressionStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    DecompressionStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TextEncoderStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TextDecoderStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Headers: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Body: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Request: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Response: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WebSocket: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WebSocketPair: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    WebSocketRequestResponsePair: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    AbortController: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    AbortSignal: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TextDecoder: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    TextEncoder: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    navigator: ClassVar[Navigator] = ... # type:ignore[assignment,unused-ignore]
    Navigator: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    URL: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    URLSearchParams: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    URLPattern: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Blob: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    File: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    FormData: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Crypto: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    SubtleCrypto: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CryptoKey: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    CacheStorage: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    Cache: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    FixedLengthStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    IdentityTransformStream: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    HTMLRewriter: ClassVar[Any] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def btoa(self, data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def atob(self, data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def setTimeout(self, callback: self__setTimeout__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def setTimeout[*Args](self, callback: self__setTimeout__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def clearTimeout(self, timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def setInterval(self, callback: self__setInterval__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def setInterval[*Args](self, callback: self__setInterval__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def clearInterval(self, timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def queueMicrotask(self, task: Callable[..., Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def structuredClone[T](self, value: T, options: StructuredSerializeOptions_iface | None = None, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def structuredClone[T](self, value: T, /, *, transfer: PyMutableSequence[Any] | None = None) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def reportError(self, error: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, init: RequestInit_iface[RequestInitCfProperties_iface] | None = None, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: RequestInitCfProperties_iface | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class scheduler(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def wait(self, delay: int | float, maybeOptions: SchedulerWaitOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def wait(self, delay: int | float, /, *, signal: AbortSignal | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Cloudflare(_JsObject): # type:ignore[misc, unused-ignore]
    compatibilityFlags: ClassVar[Record[str, bool]] = ... # type:ignore[assignment,unused-ignore]

class Response(Response_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def error(self, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def redirect(self, url: str, status: int | None = None, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def json(self, any: Any, maybeInit: (ResponseInit_iface | Response) | None = None, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def json(self, /) -> Future[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, body: BodyInit | None = None, init: ResponseInit_iface | None = None, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, body: BodyInit | None = None, /, *, status: int | None = None, statusText: str | None = None, headers: HeadersInit | None = None, cf: Any | None = None, webSocket: (WebSocket | None) | None = None, encodeBody: Literal["automatic", "manual"] | None = None) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Request[CfHostMetadata=Any, Cf=Any](Request_iface[CfHostMetadata, Cf], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, input: RequestInfo[CfProperties[Any], CfProperties[CfProperties[Any]]] | URL_, init: RequestInit_iface[Cf] | None = None, /) -> Request[CfHostMetadata, Cf]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, input: RequestInfo[CfProperties[Any], CfProperties[CfProperties[Any]]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: Cf | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Request[CfHostMetadata, Cf]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStream[R=Any](ReadableStream_iface[R], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSource: UnderlyingByteSource_iface, strategy: QueuingStrategy_iface[Uint8Array[ArrayBufferLike]] | None = None, /) -> ReadableStream[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSource: UnderlyingByteSource_iface, /, *, highWaterMark: (int | float | int) | None = None, size: Callable[[Uint8Array[ArrayBufferLike]], int | float | int] | None = None) -> ReadableStream[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSource: UnderlyingSource_iface[R] | None = None, strategy: QueuingStrategy_iface[R] | None = None, /) -> ReadableStream[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSource: UnderlyingSource_iface[R] | None = None, /, *, highWaterMark: (int | float | int) | None = None, size: Callable[[R], int | float | int] | None = None) -> ReadableStream[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WebSocket(WebSocket_iface, _JsObject): # type:ignore[misc, unused-ignore]
    READY_STATE_CONNECTING: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    CONNECTING: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    READY_STATE_OPEN: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    OPEN: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    READY_STATE_CLOSING: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    CLOSING: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    READY_STATE_CLOSED: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    CLOSED: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def new(self, url: str, protocols: (PyMutableSequence[str] | str) | None = None, /) -> WebSocket: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WebSocketPair(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Object(Object_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def getPrototypeOf(self, o: Any, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def getOwnPropertyDescriptor(self, o: Any, p: PropertyKey, /) -> PropertyDescriptor_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def getOwnPropertyNames(self, o: Any, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def create(self, o: Any | None, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def create(self, o: Any | None, properties: Object__create__Sig1__properties, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def defineProperty[T](self, o: T, p: PropertyKey, attributes: Object__defineProperty__Sig0__attributes, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def defineProperties[T](self, o: T, properties: Object__defineProperties__Sig0__properties, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def seal[T](self, o: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def freeze[T](self, f: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def freeze[T, U](self, o: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def freeze[T](self, o: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def preventExtensions[T](self, o: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isSealed(self, o: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isFrozen(self, o: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isExtensible(self, o: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def keys(self, o: Any, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def keys(self, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def assign[T, U](self, target: T, source: U, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def assign[T, U, V](self, target: T, source1: U, source2: V, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def assign[T, U, V, W](self, target: T, source1: U, source2: V, source3: W, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def assign(self, target: Any, /, *sources: Any) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def getOwnPropertySymbols(self, o: Any, /) -> JsArray[Symbol]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def is_(self, value1: Any, value2: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def setPrototypeOf(self, o: Any, proto: Any | None, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def values[T](self, o: Object__values__Sig0__o__Union0 | ArrayLike_iface[T], /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def values(self, /) -> JsArray[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def entries[T](self, o: Object__entries__Sig0__o__Union0 | ArrayLike_iface[T], /) -> JsArray[tuple[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def entries(self, /) -> JsArray[tuple[str, Any]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def getOwnPropertyDescriptors[T](self, o: T, /) -> Object__getOwnPropertyDescriptors__Sig0: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fromEntries[T=Any](self, entries: PyIterable[tuple[PropertyKey, T]], /) -> JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fromEntries(self, entries: PyIterable[PyMutableSequence[Any]], /) -> JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def hasOwn(self, o: Any, v: PropertyKey, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def groupBy[K, T](self, items: PyIterable[T], keySelector: Callable[[T, int | float], K], /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def new(self, value: Any | None = None, /) -> Object: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Function(Function_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /, *args: str) -> Callable[..., Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class String(String_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def fromCharCode(self, /, *codes: int) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def fromCodePoint(self, /, *codePoints: int) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def raw(self, template: String__raw__Sig0__template, /, *substitutions: Any) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def new(self, value: Any | None = None, /) -> String: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Boolean(Boolean_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, value: Any | None = None, /) -> Boolean: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Number(Number_iface, _JsObject): # type:ignore[misc, unused-ignore]
    MAX_VALUE: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    MIN_VALUE: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NaN: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NEGATIVE_INFINITY: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    POSITIVE_INFINITY: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    EPSILON: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    MAX_SAFE_INTEGER: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    MIN_SAFE_INTEGER: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def isFinite(self, number: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isInteger(self, number: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isNaN(self, number: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isSafeInteger(self, number: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def parseFloat(self, string: str, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def parseInt(self, string: str, radix: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def new(self, value: Any | None = None, /) -> Number: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Math(_JsObject): # type:ignore[misc, unused-ignore]
    E: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    LN10: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    LN2: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    LOG2E: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    LOG10E: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    PI: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    SQRT1_2: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    SQRT2: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def abs(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def acos(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def asin(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def atan(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def atan2(self, y: int | float, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def ceil(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def cos(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def exp(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def floor(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def log(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def max(self, /, *values: int | float) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def min(self, /, *values: int | float) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def pow(self, x: int | float, y: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def random(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def round(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def sin(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def sqrt(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def tan(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def clz32(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def imul(self, x: int | float, y: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def sign(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def log10(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def log2(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def log1p(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def expm1(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def cosh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def sinh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def tanh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def acosh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def asinh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def atanh(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def hypot(self, /, *values: int | float) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def trunc(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def fround(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def cbrt(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def f16round(self, x: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Date(Date_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def parse(self, s: str, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def UTC(self, year: int | float, monthIndex: int | float, date: int | float | None = None, hours: int | float | None = None, minutes: int | float | None = None, seconds: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def UTC(self, year: int | float, monthIndex: int | float | None = None, date: int | float | None = None, hours: int | float | None = None, minutes: int | float | None = None, seconds: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def now(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, value: int | float | str, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, year: int | float, monthIndex: int | float, date: int | float | None = None, hours: int | float | None = None, minutes: int | float | None = None, seconds: int | float | None = None, ms: int | float | None = None, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, value: int | float | str | Date, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RegExp(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, pattern: RegExp | str, /) -> RegExp: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, pattern: str, flags: str | None = None, /) -> RegExp: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, pattern: RegExp | str, flags: str | None = None, /) -> RegExp: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Error(Error_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def isError(self, error: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> Error: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> Error: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> Error: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EvalError(EvalError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> EvalError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> EvalError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> EvalError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RangeError(RangeError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> RangeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> RangeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> RangeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReferenceError(ReferenceError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> ReferenceError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> ReferenceError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> ReferenceError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SyntaxError(SyntaxError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> SyntaxError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> SyntaxError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> SyntaxError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TypeError(TypeError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> TypeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> TypeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> TypeError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URIError(URIError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /) -> URIError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, options: ErrorOptions_iface | None = None, /) -> URIError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, message: str | None = None, /, *, cause: Any | None = None) -> URIError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class JSON(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def parse(self, text: str, reviver: Callable[[Any, str, Any], Any] | None = None, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def stringify(self, value: Any, replacer: Callable[[Any, str, Any], Any] | None = None, space: str | int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def stringify(self, value: Any, replacer: PyMutableSequence[(int | float | str)] | None = None, space: str | int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Array(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def isArray(self, arg: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, /, *, length: int) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T, U](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], U], thisArg: Any | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, iterable: PyIterable[T] | ArrayLike_iface[T], /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T, U](self, iterable: PyIterable[T] | ArrayLike_iface[T], mapfn: Callable[[T, int], U], thisArg: Any | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def of[T](self, /, *items: T) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fromAsync[T](self, iterableOrArrayLike: PyAsyncIterable[T] | PyIterable[T | PromiseLike_iface[T]] | ArrayLike_iface[T | PromiseLike_iface[T]], /) -> Future[JsArray[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def fromAsync[T, U](self, iterableOrArrayLike: PyAsyncIterable[T] | PyIterable[T] | ArrayLike_iface[T], mapFn: Callable[[Awaited[T], int], U], thisArg: Any | None = None, /) -> Future[JsArray[Awaited[U]]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, arrayLength: int | None = None, /) -> JsArray[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new[T](self, arrayLength: int, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new[T](self, /, *items: T) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ArrayBuffer(ArrayBuffer_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def isView(self, arg: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, byteLength: int, /) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, byteLength: int, /, *, maxByteLength: int | None = None) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DataView[TArrayBuffer](DataView_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, byteLength: int | None = None, /) -> DataView[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int8Array[TArrayBuffer](Int8Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int8Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint8Array[TArrayBuffer](Uint8Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint8Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint8ClampedArray[TArrayBuffer](Uint8ClampedArray_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint8ClampedArray[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int16Array[TArrayBuffer](Int16Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint16Array[TArrayBuffer](Uint16Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int32Array[TArrayBuffer](Int32Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint32Array[TArrayBuffer](Uint32Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int], int], thisArg: Any | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int], /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float32Array[TArrayBuffer](Float32Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int | float) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int | float], /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int | float) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int | float], int | float], thisArg: Any | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int | float], int | float] | None = None, thisArg: Any | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int | float, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float], /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int | float) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float] | ArrayBuffer, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float64Array[TArrayBuffer](Float64Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int | float) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int | float], /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int | float) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int | float], int | float], thisArg: Any | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int | float], int | float] | None = None, thisArg: Any | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int | float, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float], /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, length: int | float) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float] | ArrayBuffer, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, elements: PyIterable[int | float], /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WeakMap[K, V](WeakMap_iface[K, V], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, entries: PyMutableSequence[(tuple[K, V])] | None = None, /) -> WeakMap[K, V]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, iterable: PyIterable[tuple[K, V]], /) -> WeakMap[K, V]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Set[T](Set_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, values: PyMutableSequence[T] | None = None, /) -> Set[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, iterable: PyIterable[T] | None = None, /) -> Set[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WeakSet[T](WeakSet_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, values: PyMutableSequence[T] | None = None, /) -> WeakSet[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, iterable: PyIterable[T], /) -> WeakSet[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Symbol(Symbol_iface, _JsObject): # type:ignore[misc, unused-ignore]
    iterator: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    hasInstance: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    isConcatSpreadable: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    match: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    replace: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    search: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    species: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    split: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    toPrimitive: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    toStringTag: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    unscopables: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    asyncIterator: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    matchAll: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    dispose: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    asyncDispose: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    metadata: ClassVar[Symbol] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def for_(self, key: str, /) -> Symbol: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def keyFor(self, sym: Symbol, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Proxy(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def revocable[T](self, target: T, handler: ProxyHandler_iface[T], /) -> Proxy__revocable__Sig0[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def revocable[T](self, target: T, /) -> Proxy__revocable__Sig0[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new[T](self, target: T, handler: ProxyHandler_iface[T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new[T](self, target: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SharedArrayBuffer(SharedArrayBuffer_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, byteLength: int | None = None, /) -> SharedArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, byteLength: int, /, *, maxByteLength: int | None = None) -> SharedArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Atomics(_JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def add(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def add(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def and_(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def and_(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def compareExchange(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, expectedValue: int | float, replacementValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def compareExchange(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, expectedValue: int, replacementValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def exchange(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def exchange(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def isLockFree(self, size: int | float, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def load(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def load(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def or_(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def or_(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def store(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def store(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def sub(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def sub(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def wait(self, typedArray: Int32Array[ArrayBufferLike], index: int | float, value: int | float, timeout: int | float | None = None, /) -> Literal["ok", "not-equal", "timed-out"]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def wait(self, typedArray: BigInt64Array[ArrayBufferLike], index: int | float, value: int, timeout: int | float | None = None, /) -> Literal["ok", "not-equal", "timed-out"]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def notify(self, typedArray: Int32Array[ArrayBufferLike], index: int | float, count: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def xor(self, typedArray: Int8Array[ArrayBufferLike] | Uint8Array[ArrayBufferLike] | Int16Array[ArrayBufferLike] | Uint16Array[ArrayBufferLike] | Int32Array[ArrayBufferLike] | Uint32Array[ArrayBufferLike], index: int | float, value: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def xor(self, typedArray: BigInt64Array[ArrayBufferLike] | BigUint64Array[ArrayBufferLike], index: int | float, value: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def waitAsync(self, typedArray: Int32Array[ArrayBufferLike], index: int | float, value: int | float, timeout: int | float | None = None, /) -> Atomics__waitAsync__Sig0__Union0 | Atomics__waitAsync__Sig0__Union1: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def waitAsync(self, typedArray: BigInt64Array[ArrayBufferLike], index: int | float, value: int, timeout: int | float | None = None, /) -> Atomics__waitAsync__Sig1__Union0 | Atomics__waitAsync__Sig1__Union1: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def pause(self, n: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigInt(BigInt_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def asIntN(self, bits: int | float, int: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def asUintN(self, bits: int | float, int: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigInt64Array[TArrayBuffer](BigInt64Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[U](self, arrayLike: ArrayLike_iface[U], mapfn: Callable[[U, int], int], thisArg: Any | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int], /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | PyIterable[int], /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> BigInt64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigUint64Array[TArrayBuffer](BigUint64Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int], /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[U](self, arrayLike: ArrayLike_iface[U], mapfn: Callable[[U, int], int], thisArg: Any | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int], /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int], int] | None = None, thisArg: Any | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | PyIterable[int], /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> BigUint64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | None = None, length: int | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int] | ArrayBuffer, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AggregateError(AggregateError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, errors: PyIterable[Any], message: str | None = None, /) -> AggregateError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, errors: PyIterable[Any], message: str | None = None, options: ErrorOptions_iface | None = None, /) -> AggregateError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, errors: PyIterable[Any], message: str | None = None, /, *, cause: Any | None = None) -> AggregateError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WeakRef[T](WeakRef_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, target: T, /) -> WeakRef[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FinalizationRegistry[T](FinalizationRegistry_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, cleanupCallback: Callable[[T], None], /) -> FinalizationRegistry[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SuppressedError(SuppressedError_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, error: Any, suppressed: Any, message: str | None = None, /) -> SuppressedError: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DisposableStack(DisposableStack_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> DisposableStack: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AsyncDisposableStack(AsyncDisposableStack_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> AsyncDisposableStack: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float16Array[TArrayBuffer=ArrayBufferLike](Float16Array_iface[TArrayBuffer], _JsObject): # type:ignore[misc, unused-ignore]
    BYTES_PER_ELEMENT: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def of(self, /, *items: int | float) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, arrayLike: ArrayLike_iface[int | float], /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, /, *, length: int | float) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, arrayLike: ArrayLike_iface[T], mapfn: Callable[[T, int | float], int | float], thisArg: Any | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_(self, elements: PyIterable[int | float], /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def from_[T](self, elements: PyIterable[T], mapfn: Callable[[T, int | float], int | float] | None = None, thisArg: Any | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, length: int | float | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float] | PyIterable[int | float], /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: TArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, buffer: ArrayBuffer, byteOffset: int | float | None = None, length: int | float | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, array: ArrayLike_iface[int | float] | ArrayBuffer, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DOMException_iface(Error_iface): # type:ignore[misc, unused-ignore]
    @property
    def message(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def name(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def code(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DOMException(DOMException_iface, _JsObject): # type:ignore[misc, unused-ignore]
    INDEX_SIZE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    DOMSTRING_SIZE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    HIERARCHY_REQUEST_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    WRONG_DOCUMENT_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INVALID_CHARACTER_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NO_DATA_ALLOWED_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NO_MODIFICATION_ALLOWED_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NOT_FOUND_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NOT_SUPPORTED_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INUSE_ATTRIBUTE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INVALID_STATE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    SYNTAX_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INVALID_MODIFICATION_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NAMESPACE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INVALID_ACCESS_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    VALIDATION_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    TYPE_MISMATCH_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    SECURITY_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    NETWORK_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    ABORT_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    URL_MISMATCH_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    QUOTA_EXCEEDED_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    TIMEOUT_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    INVALID_NODE_TYPE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    DATA_CLONE_ERR: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def new(self, message: str | None = None, name: str | None = None, /) -> DOMException_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WorkerGlobalScope_iface(EventTarget_iface[WorkerGlobalScopeEventMap], Protocol): # type:ignore[misc, unused-ignore]
    EventTarget: Any = ... # type:ignore[assignment,unused-ignore]

class WorkerGlobalScope(WorkerGlobalScope_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Navigator_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def userAgent(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def hardwareConcurrency(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def language(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def languages(self, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sendBeacon(self, url: str, body: BodyInit | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Navigator(Navigator_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class DurableObjectNamespace_iface[T=None](Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def newUniqueId(self, options: DurableObjectNamespaceNewUniqueIdOptions_iface | None = None, /) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def newUniqueId(self, /, *, jurisdiction: DurableObjectJurisdiction | None = None) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def idFromName(self, name: str, /) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def idFromString(self, id: str, /) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get(self, id: DurableObjectId_iface, options: DurableObjectNamespaceGetDurableObjectOptions_iface | None = None, /) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get(self, id: DurableObjectId_iface, /, *, locationHint: DurableObjectLocationHint | None = None) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getByName(self, name: str, options: DurableObjectNamespaceGetDurableObjectOptions_iface | None = None, /) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getByName(self, name: str, /, *, locationHint: DurableObjectLocationHint | None = None) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def jurisdiction(self, jurisdiction: DurableObjectJurisdiction, /) -> DurableObjectNamespace[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__(self, id: DurableObjectId_iface, options: DurableObjectNamespaceGetDurableObjectOptions_iface | None = None, /) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__(self, id: DurableObjectId_iface, /, *, locationHint: DurableObjectLocationHint | None = None) -> DurableObjectStub[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectNamespace[T=None](DurableObjectNamespace_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class WebSocketRequestResponsePair_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class WebSocketRequestResponsePair(WebSocketRequestResponsePair_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, request: str, response: str, /) -> WebSocketRequestResponsePair_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Event_iface(Protocol): # type:ignore[misc, unused-ignore]
    def stopImmediatePropagation(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def preventDefault(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def stopPropagation(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def composedPath(self, /) -> JsArray[EventTarget[Record[str, Event]]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Event(Event_iface, _JsObject): # type:ignore[misc, unused-ignore]
    NONE: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    CAPTURING_PHASE: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    AT_TARGET: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    BUBBLING_PHASE: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, init: EventInit_iface | None = None, /) -> Event_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, /, *, bubbles: bool | None = None, cancelable: bool | None = None, composed: bool | None = None) -> Event_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EventTarget_iface[EventMap=Record[str, Event]](Protocol): # type:ignore[misc, unused-ignore]
    
    
    def dispatchEvent(self, event: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EventTarget[EventMap=Record[str, Event]](EventTarget_iface[EventMap], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> EventTarget_iface[EventMap]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AbortController_iface(Protocol): # type:ignore[misc, unused-ignore]
    def abort(self, reason: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AbortController(AbortController_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> AbortController_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AbortSignal_iface(EventTarget_iface[Record[str, Event]], Protocol): # type:ignore[misc, unused-ignore]
    def throwIfAborted(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AbortSignal(AbortSignal_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def abort(self, reason: Any | None = None, /) -> AbortSignal: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def timeout(self, delay: int | float, /) -> AbortSignal: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def any(self, signals: PyMutableSequence[AbortSignal], /) -> AbortSignal: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ExtendableEvent_iface(Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    def waitUntil(self, promise: Future[Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ExtendableEvent(ExtendableEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class CustomEvent_iface[T=Any](Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class CustomEvent[T=Any](CustomEvent_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, init: CustomEventCustomEventInit_iface | None = None, /) -> CustomEvent_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, /, *, bubbles: bool | None = None, cancelable: bool | None = None, composed: bool | None = None, detail: Any | None = None) -> CustomEvent_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Blob_iface(Protocol): # type:ignore[misc, unused-ignore]
    def slice(self, start: int | float | None = None, end: int | float | None = None, type: str | None = None, /) -> Blob: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def arrayBuffer(self, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def bytes(self, /) -> Future[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def text(self, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def stream(self, /) -> ReadableStream[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Blob(Blob_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, type: PyMutableSequence[((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob)] | None = None, options: BlobOptions_iface | None = None, /) -> Blob_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type_: PyMutableSequence[((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob)] | None = None, /, *, type: str | None = None) -> Blob_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class File_iface(Blob_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class File(File_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, bits: PyMutableSequence[((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob)] | None, name: str, options: FileOptions_iface | None = None, /) -> File_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, bits: PyMutableSequence[((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob)] | None, name: str, /, *, type: str | None = None, lastModified: int | float | None = None) -> File_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CacheStorage_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def default(self, /) -> Cache: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def open(self, cacheName: str, /) -> Future[Cache]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CacheStorage(CacheStorage_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Cache_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def delete(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, options: CacheQueryOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, ignoreMethod: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def match(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, options: CacheQueryOptions_iface | None = None, /) -> Future[Response | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def match(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, ignoreMethod: bool | None = None) -> Future[Response | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def put(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, response: Response, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, options: CacheQueryOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, request: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, ignoreMethod: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Cache(Cache_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Crypto_iface(Protocol): # type:ignore[misc, unused-ignore]
    DigestStream: Any = ... # type:ignore[assignment,unused-ignore]
    def getRandomValues[T](self, buffer: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def randomUUID(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Crypto(Crypto_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class SubtleCrypto_iface(Protocol): # type:ignore[misc, unused-ignore]
    def encrypt(self, algorithm: str | SubtleCryptoEncryptAlgorithm_iface, key: CryptoKey, plainText: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def decrypt(self, algorithm: str | SubtleCryptoEncryptAlgorithm_iface, key: CryptoKey, cipherText: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sign(self, algorithm: str | SubtleCryptoSignAlgorithm_iface, key: CryptoKey, data: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def verify(self, algorithm: str | SubtleCryptoSignAlgorithm_iface, key: CryptoKey, signature: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], data: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def digest(self, algorithm: str | SubtleCryptoHashAlgorithm_iface, data: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def generateKey(self, algorithm: str | SubtleCryptoGenerateKeyAlgorithm_iface, extractable: bool, keyUsages: PyMutableSequence[str], /) -> Future[CryptoKey | CryptoKeyPair_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deriveKey(self, algorithm: str | SubtleCryptoDeriveKeyAlgorithm_iface, baseKey: CryptoKey, derivedKeyAlgorithm: str | SubtleCryptoImportKeyAlgorithm_iface, extractable: bool, keyUsages: PyMutableSequence[str], /) -> Future[CryptoKey]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deriveBits(self, algorithm: str | SubtleCryptoDeriveKeyAlgorithm_iface, baseKey: CryptoKey, length: int | float | None = None, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def importKey(self, format: str, keyData: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | JsonWebKey_iface, algorithm: str | SubtleCryptoImportKeyAlgorithm_iface, extractable: bool, keyUsages: PyMutableSequence[str], /) -> Future[CryptoKey]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def exportKey(self, format: str, key: CryptoKey, /) -> Future[ArrayBuffer | JsonWebKey_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def wrapKey(self, format: str, key: CryptoKey, wrappingKey: CryptoKey, wrapAlgorithm: str | SubtleCryptoEncryptAlgorithm_iface, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def unwrapKey(self, format: str, wrappedKey: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], unwrappingKey: CryptoKey, unwrapAlgorithm: str | SubtleCryptoEncryptAlgorithm_iface, unwrappedKeyAlgorithm: str | SubtleCryptoImportKeyAlgorithm_iface, extractable: bool, keyUsages: PyMutableSequence[str], /) -> Future[CryptoKey]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def timingSafeEqual(self, a: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], b: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SubtleCrypto(SubtleCrypto_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class CryptoKey_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def type(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def extractable(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def algorithm(self, /) -> CryptoKeyKeyAlgorithm_iface | CryptoKeyAesKeyAlgorithm_iface | CryptoKeyHmacKeyAlgorithm_iface | CryptoKeyRsaKeyAlgorithm_iface | CryptoKeyEllipticKeyAlgorithm_iface | CryptoKeyArbitraryKeyAlgorithm_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def usages(self, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CryptoKey(CryptoKey_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class DigestStream_iface(WritableStream_iface[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]], Protocol): # type:ignore[misc, unused-ignore]
    @property
    def digest(self, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DigestStream(DigestStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, algorithm: str | SubtleCryptoHashAlgorithm_iface, /) -> DigestStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextDecoder_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def decode(self, input: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = None, options: TextDecoderDecodeOptions_iface | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def decode(self, input: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = None, /, *, stream: bool) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextDecoder(TextDecoder_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, label: str | None = None, options: TextDecoderConstructorOptions_iface | None = None, /) -> TextDecoder_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, label: str | None = None, /, *, fatal: bool, ignoreBOM: bool) -> TextDecoder_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextEncoder_iface(Protocol): # type:ignore[misc, unused-ignore]
    def encode(self, input: str | None = None, /) -> Uint8Array[ArrayBufferLike]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def encodeInto(self, input: str, buffer: Uint8Array[ArrayBufferLike], /) -> TextEncoderEncodeIntoResult_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextEncoder(TextEncoder_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> TextEncoder_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ErrorEvent_iface(Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ErrorEvent(ErrorEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, init: ErrorEventErrorEventInit_iface | None = None, /) -> ErrorEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, /, *, message: str | None = None, filename: str | None = None, lineno: int | float | None = None, colno: int | float | None = None, error: Any | None = None) -> ErrorEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class MessageEvent_iface(Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def data(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def origin(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def lastEventId(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def source(self, /) -> MessagePort | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def ports(self, /) -> JsArray[MessagePort]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class MessageEvent(MessageEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, initializer: MessageEventInit_iface, /) -> MessageEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, /, *, data: ArrayBuffer | str) -> MessageEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class PromiseRejectionEvent_iface(Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def promise(self, /) -> Future[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def reason(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class PromiseRejectionEvent(PromiseRejectionEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class FormData_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def append(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def append(self, name: str, value: Blob, filename: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, name: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def get(self, name: str, /) -> (File | str) | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getAll(self, name: str, /) -> JsArray[(File | str)]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, name: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def set(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def set(self, name: str, value: Blob, filename: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> JsIterator[tuple[str, File | str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> JsIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> JsIterator[(File | str)]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach[This=Any](self, callback: Callable[[This, File | str, str, FormData], None], thisArg: This | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[tuple[str, File | str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, name: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, name: str, /) -> (File | str) | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __setitem__(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __setitem__(self, name: str, value: Blob, filename: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, name: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FormData(FormData_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> FormData_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class HTMLRewriter_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def on(self, selector: str, handlers: HTMLRewriterElementContentHandlers_iface, /) -> HTMLRewriter: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def on(self, selector: str, /) -> HTMLRewriter: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def onDocument(self, handlers: HTMLRewriterDocumentContentHandlers_iface, /) -> HTMLRewriter: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def onDocument(self, /) -> HTMLRewriter: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def transform(self, response: Response, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class HTMLRewriter(HTMLRewriter_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> HTMLRewriter_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FetchEvent_iface(ExtendableEvent_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def request(self, /) -> Request[Any, CfProperties[Any]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def respondWith(self, promise: Response | Future[Response], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def passThroughOnException(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FetchEvent(FetchEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Headers_iface(JsIterable[tuple[str, str]]): # type:ignore[misc, unused-ignore]
    def get(self, name: str, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getAll(self, name: str, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getSetCookie(self, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, name: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def append(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, name: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach[This=Any](self, callback: Callable[[This, str, str, Headers], None], thisArg: This | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> JsIterator[tuple[str, str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> JsIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> JsIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[tuple[str, str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, name: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, name: str, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, name: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Headers(Headers_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, init: HeadersInit | None = None, /) -> Headers_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Body_iface(Protocol): # type:ignore[misc, unused-ignore]
    def arrayBuffer(self, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def bytes(self, /) -> Future[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def text(self, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def json[T](self, /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def formData(self, /) -> Future[FormData]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def blob(self, /) -> Future[Blob]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Body(Body_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class R2Bucket_iface(Protocol): # type:ignore[misc, unused-ignore]
    def head(self, key: str, /) -> Future[R2Object | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get(self, key: str, options: R2Bucket__get__Sig0__options, /) -> Future[R2ObjectBody_iface | R2Object | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get(self, key: str, options: R2GetOptions_iface | None = None, /) -> Future[R2ObjectBody_iface | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get(self, key: str, /, *, onlyIf: (R2Conditional_iface | Headers) | None = None, range: (R2Range | Headers) | None = None, ssecKey: (ArrayBuffer | str) | None = None) -> Future[R2ObjectBody_iface | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put(self, key: str, value: ReadableStream[Any] | ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike] | str | Blob | None, options: R2Bucket__put__Sig0__options | None = None, /) -> Future[R2Object | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put(self, key: str, value: ReadableStream[Any] | ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike] | str | Blob | None, options: R2PutOptions_iface | None = None, /) -> Future[R2Object]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put(self, key: str, value: ReadableStream[Any] | ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike] | str | Blob | None, /, *, onlyIf: (R2Conditional_iface | Headers) | None = None, httpMetadata: (R2HTTPMetadata_iface | Headers) | None = None, customMetadata: Record[str, str] | None = None, md5: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = None, sha1: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = None, sha256: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = None, sha384: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = None, sha512: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = None, storageClass: str | None = None, ssecKey: (ArrayBuffer | str) | None = None) -> Future[R2Object]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def createMultipartUpload(self, key: str, options: R2MultipartOptions_iface | None = None, /) -> Future[R2MultipartUpload_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def createMultipartUpload(self, key: str, /, *, httpMetadata: (R2HTTPMetadata_iface | Headers) | None = None, customMetadata: Record[str, str] | None = None, storageClass: str | None = None, ssecKey: (ArrayBuffer | str) | None = None) -> Future[R2MultipartUpload_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def resumeMultipartUpload(self, key: str, uploadId: str, /) -> R2MultipartUpload_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, keys: str | PyMutableSequence[str], /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list(self, options: R2ListOptions_iface | None = None, /) -> Future[R2Objects]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list(self, /, *, limit: int | float | None = None, prefix: str | None = None, cursor: str | None = None, delimiter: str | None = None, startAfter: str | None = None, include: PyMutableSequence[(Literal["httpMetadata", "customMetadata"])] | None = None) -> Future[R2Objects]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__(self, key: str, options: R2Bucket____getitem____Sig0__options, /) -> Future[R2ObjectBody_iface | R2Object | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__(self, key: str, options: R2GetOptions_iface | None = None, /) -> Future[R2ObjectBody_iface | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__(self, key: str, /, *, onlyIf: (R2Conditional_iface | Headers) | None = None, range: (R2Range | Headers) | None = None, ssecKey: (ArrayBuffer | str) | None = None) -> Future[R2ObjectBody_iface | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, keys: str | PyMutableSequence[str], /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2Bucket(R2Bucket_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class R2Object_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def key(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def version(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def size(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def etag(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def httpEtag(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def checksums(self, /) -> R2Checksums_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def uploaded(self, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def httpMetadata(self, /) -> R2HTTPMetadata_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def customMetadata(self, /) -> Record[str, str] | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def range(self, /) -> R2Range | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def storageClass(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def ssecKeyMd5(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def writeHttpMetadata(self, headers: Headers, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2Object(R2Object_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class ScheduledEvent_iface(ExtendableEvent_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def scheduledTime(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def cron(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def noRetry(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ScheduledEvent(ScheduledEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class ReadableStreamDefaultReader_iface[R=Any](Protocol): # type:ignore[misc, unused-ignore]
    def cancel(self, reason: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def read(self, /) -> Future[ReadableStreamReadResult[R]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def releaseLock(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamDefaultReader[R=Any](ReadableStreamDefaultReader_iface[R], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, stream: ReadableStream[Any], /) -> ReadableStreamDefaultReader_iface[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamBYOBReader_iface(Protocol): # type:ignore[misc, unused-ignore]
    def cancel(self, reason: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def read[T](self, view: T, /) -> Future[ReadableStreamReadResult[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def releaseLock(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def readAtLeast[T](self, minElements: int | float, view: T, /) -> Future[ReadableStreamReadResult[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamBYOBReader(ReadableStreamBYOBReader_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, stream: ReadableStream[Any], /) -> ReadableStreamBYOBReader_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamBYOBRequest_iface(Protocol): # type:ignore[misc, unused-ignore]
    def respond(self, bytesWritten: int | float, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def respondWithNewView(self, view: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamBYOBRequest(ReadableStreamBYOBRequest_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class ReadableStreamDefaultController_iface[R=Any](Protocol): # type:ignore[misc, unused-ignore]
    def close(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def enqueue(self, chunk: R | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def error(self, reason: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamDefaultController[R=Any](ReadableStreamDefaultController_iface[R], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class ReadableByteStreamController_iface(Protocol): # type:ignore[misc, unused-ignore]
    def close(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def enqueue(self, chunk: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def error(self, reason: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableByteStreamController(ReadableByteStreamController_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class WritableStreamDefaultController_iface(Protocol): # type:ignore[misc, unused-ignore]
    def error(self, reason: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WritableStreamDefaultController(WritableStreamDefaultController_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class TransformStreamDefaultController_iface[O=Any](Protocol): # type:ignore[misc, unused-ignore]
    def enqueue(self, chunk: O | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def error(self, reason: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def terminate(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TransformStreamDefaultController[O=Any](TransformStreamDefaultController_iface[O], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class WritableStream_iface[W=Any](Protocol): # type:ignore[misc, unused-ignore]
    def abort(self, reason: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def close(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getWriter(self, /) -> WritableStreamDefaultWriter[W]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WritableStream[W=Any](WritableStream_iface[W], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSink: UnderlyingSink_iface[Any] | None = None, queuingStrategy: QueuingStrategy_iface[Any] | None = None, /) -> WritableStream_iface[W]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, underlyingSink: UnderlyingSink_iface[Any] | None = None, /, *, highWaterMark: (int | float | int) | None = None, size: Callable[[Any], int | float | int] | None = None) -> WritableStream_iface[W]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WritableStreamDefaultWriter_iface[W=Any](Protocol): # type:ignore[misc, unused-ignore]
    def abort(self, reason: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def close(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def write(self, chunk: W | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def releaseLock(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WritableStreamDefaultWriter[W=Any](WritableStreamDefaultWriter_iface[W], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, stream: WritableStream[Any], /) -> WritableStreamDefaultWriter_iface[W]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TransformStream_iface[I=Any, O=Any](Protocol): # type:ignore[misc, unused-ignore]
    pass

class TransformStream[I=Any, O=Any](TransformStream_iface[I, O], _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, transformer: Transformer_iface[I, O] | None = None, writableStrategy: QueuingStrategy_iface[I] | None = None, readableStrategy: QueuingStrategy_iface[O] | None = None, /) -> TransformStream_iface[I, O]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, transformer: Transformer_iface[I, O] | None = None, writableStrategy: QueuingStrategy_iface[I] | None = None, /, *, highWaterMark: (int | float | int) | None = None, size: Callable[[O], int | float | int] | None = None) -> TransformStream_iface[I, O]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FixedLengthStream_iface(IdentityTransformStream_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class FixedLengthStream(FixedLengthStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, expectedLength: int | float | int, queuingStrategy: IdentityTransformStreamQueuingStrategy_iface | None = None, /) -> FixedLengthStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, expectedLength: int | float | int, /, *, highWaterMark: (int | float | int) | None = None) -> FixedLengthStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class IdentityTransformStream_iface(TransformStream_iface[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], Uint8Array[ArrayBufferLike]], Protocol): # type:ignore[misc, unused-ignore]
    pass

class IdentityTransformStream(IdentityTransformStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, queuingStrategy: IdentityTransformStreamQueuingStrategy_iface | None = None, /) -> IdentityTransformStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, highWaterMark: (int | float | int) | None = None) -> IdentityTransformStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CompressionStream_iface(TransformStream_iface[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], Uint8Array[ArrayBufferLike]], Protocol): # type:ignore[misc, unused-ignore]
    pass

class CompressionStream(CompressionStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, format: Literal["gzip", "deflate", "deflate-raw"], /) -> CompressionStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DecompressionStream_iface(TransformStream_iface[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], Uint8Array[ArrayBufferLike]], Protocol): # type:ignore[misc, unused-ignore]
    pass

class DecompressionStream(DecompressionStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, format: Literal["gzip", "deflate", "deflate-raw"], /) -> DecompressionStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextEncoderStream_iface(TransformStream_iface[str, Uint8Array[ArrayBufferLike]], Protocol): # type:ignore[misc, unused-ignore]
    pass

class TextEncoderStream(TextEncoderStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> TextEncoderStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextDecoderStream_iface(TransformStream_iface[ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike], str], Protocol): # type:ignore[misc, unused-ignore]
    pass

class TextDecoderStream(TextDecoderStream_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, label: str | None = None, options: TextDecoderStreamTextDecoderStreamInit_iface | None = None, /) -> TextDecoderStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, label: str | None = None, /, *, fatal: bool | None = None, ignoreBOM: bool | None = None) -> TextDecoderStream_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ByteLengthQueuingStrategy_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ByteLengthQueuingStrategy(ByteLengthQueuingStrategy_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, init: QueuingStrategyInit_iface, /) -> ByteLengthQueuingStrategy_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, highWaterMark: int | float) -> ByteLengthQueuingStrategy_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CountQueuingStrategy_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class CountQueuingStrategy(CountQueuingStrategy_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, init: QueuingStrategyInit_iface, /) -> CountQueuingStrategy_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, /, *, highWaterMark: int | float) -> CountQueuingStrategy_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TailEvent_iface(ExtendableEvent_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def events(self, /) -> JsArray[TraceItem_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def traces(self, /) -> JsArray[TraceItem_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TailEvent(TailEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class URL_iface(Protocol): # type:ignore[misc, unused-ignore]
    def toJSON(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URL(URL_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def canParse(self, url: str, base: str | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def parse(self, url: str, base: str | None = None, /) -> URL_ | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def createObjectURL(self, object: File | Blob, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def revokeObjectURL(self, object_url: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    def new(self, url: str | URL_, base: str | URL_ | None = None, /) -> URL_: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URLSearchParams_iface(Protocol): # type:ignore[misc, unused-ignore]
    def append(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, name: str, value: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def get(self, name: str, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getAll(self, name: str, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, name: str, value: str | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> JsIterator[tuple[str, str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> JsIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> JsIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach[This=Any](self, callback: Callable[[This, str, str, URLSearchParams], None], thisArg: This | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[tuple[str, str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, name: str, value: str | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, name: str, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, name: str, value: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, name: str, value: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URLSearchParams(URLSearchParams_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, init: (PyIterable[PyIterable[str]] | Record[str, str] | str) | None = None, /) -> URLSearchParams_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URLPattern_iface(Protocol): # type:ignore[misc, unused-ignore]
    def test(self, input: (str | URLPatternInit_iface) | None = None, baseURL: str | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def exec(self, input: (str | URLPatternInit_iface) | None = None, baseURL: str | None = None, /) -> URLPatternResult_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URLPattern(URLPattern_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, input: (str | URLPatternInit_iface) | None = None, baseURL: (str | URLPatternOptions_iface) | None = None, patternOptions: URLPatternOptions_iface | None = None, /) -> URLPattern_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, input: (str | URLPatternInit_iface) | None = None, baseURL: (str | URLPatternOptions_iface) | None = None, /, *, ignoreCase: bool | None = None) -> URLPattern_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CloseEvent_iface(Event_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def code(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def reason(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def wasClean(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CloseEvent(CloseEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, initializer: CloseEventInit_iface | None = None, /) -> CloseEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, type: str, /, *, code: int | float | None = None, reason: str | None = None, wasClean: bool | None = None) -> CloseEvent_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SqlStorageStatement_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class SqlStorageStatement(SqlStorageStatement_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class SqlStorageCursor_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    columnNames: JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    def next(self, /) -> SqlStorageCursor__next__Sig0__Union0[T] | SqlStorageCursor__next__Sig0__Union1: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toArray(self, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def one(self, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def raw[U](self, /) -> JsIterator[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SqlStorageCursor[T](SqlStorageCursor_iface[T], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class EventSource_iface(EventTarget_iface[Record[str, Event]], Protocol): # type:ignore[misc, unused-ignore]
    def close(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EventSource(EventSource_iface, _JsObject): # type:ignore[misc, unused-ignore]
    CONNECTING: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    OPEN: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    CLOSED: ClassVar[int | float] = ... # type:ignore[assignment,unused-ignore]
    @classmethod
    def from_(self, stream: ReadableStream[Any], /) -> EventSource: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, url: str, init: EventSourceEventSourceInit_iface | None = None, /) -> EventSource_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @classmethod
    @overload
    def new(self, url: str, /, *, withCredentials: bool | None = None, fetcher: Fetcher[None, Never] | None = None) -> EventSource_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class MessagePort_iface(EventTarget_iface[Record[str, Event]], Protocol): # type:ignore[misc, unused-ignore]
    def postMessage(self, data: Any | None = None, options: (PyMutableSequence[Any] | MessagePortPostMessageOptions_iface) | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def close(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def start(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class MessagePort(MessagePort_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class MessageChannel_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def port1(self, /) -> MessagePort: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def port2(self, /) -> MessagePort: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class MessageChannel(MessageChannel_iface, _JsObject): # type:ignore[misc, unused-ignore]
    @classmethod
    def new(self, /) -> MessageChannel_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Performance_iface(Protocol): # type:ignore[misc, unused-ignore]
    def now(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Performance(Performance_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiImageClassification_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiImageClassificationInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiImageClassificationOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiImageClassification(BaseAiImageClassification_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiImageToText_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiImageToTextInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiImageToTextOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiImageToText(BaseAiImageToText_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiImageTextToText_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiImageTextToTextInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiImageTextToTextOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiImageTextToText(BaseAiImageTextToText_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiMultimodalEmbeddings_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiImageTextToTextInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiImageTextToTextOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiMultimodalEmbeddings(BaseAiMultimodalEmbeddings_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiObjectDetection_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiObjectDetectionInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiObjectDetectionOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiObjectDetection(BaseAiObjectDetection_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiSentenceSimilarity_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiSentenceSimilarityInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiSentenceSimilarityOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiSentenceSimilarity(BaseAiSentenceSimilarity_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiAutomaticSpeechRecognition_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiAutomaticSpeechRecognitionInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiAutomaticSpeechRecognitionOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiAutomaticSpeechRecognition(BaseAiAutomaticSpeechRecognition_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiSummarization_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiSummarizationInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiSummarizationOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiSummarization(BaseAiSummarization_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTextClassification_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTextClassificationInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTextClassificationOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTextClassification(BaseAiTextClassification_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTextEmbeddings_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTextEmbeddingsInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTextEmbeddingsOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTextEmbeddings(BaseAiTextEmbeddings_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTextGeneration_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTextGenerationInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTextGenerationOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTextGeneration(BaseAiTextGeneration_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTextToSpeech_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTextToSpeechInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTextToSpeechOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTextToSpeech(BaseAiTextToSpeech_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTextToImage_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTextToImageInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTextToImageOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTextToImage(BaseAiTextToImage_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class BaseAiTranslation_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: AiTranslationInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: AiTranslationOutput = ... # type:ignore[assignment,unused-ignore]

class BaseAiTranslation(BaseAiTranslation_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Baai_Bge_Base_En_V1_5_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Baai_Bge_Base_En_V1_5_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Baai_Bge_Base_En_V1_5_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Baai_Bge_Base_En_V1_5(Base_Ai_Cf_Baai_Bge_Base_En_V1_5_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Openai_Whisper_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Openai_Whisper_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Openai_Whisper_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Openai_Whisper(Base_Ai_Cf_Openai_Whisper_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Meta_M2M100_1_2B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Meta_M2M100_1_2B_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Meta_M2M100_1_2B_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Meta_M2M100_1_2B(Base_Ai_Cf_Meta_M2M100_1_2B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Baai_Bge_Small_En_V1_5_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Baai_Bge_Small_En_V1_5_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Baai_Bge_Small_En_V1_5_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Baai_Bge_Small_En_V1_5(Base_Ai_Cf_Baai_Bge_Small_En_V1_5_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Baai_Bge_Large_En_V1_5_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Baai_Bge_Large_En_V1_5_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Baai_Bge_Large_En_V1_5_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Baai_Bge_Large_En_V1_5(Base_Ai_Cf_Baai_Bge_Large_En_V1_5_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Unum_Uform_Gen2_Qwen_500M_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Unum_Uform_Gen2_Qwen_500M(Base_Ai_Cf_Unum_Uform_Gen2_Qwen_500M_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Openai_Whisper_Tiny_En_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Openai_Whisper_Tiny_En_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Openai_Whisper_Tiny_En_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Openai_Whisper_Tiny_En(Base_Ai_Cf_Openai_Whisper_Tiny_En_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Openai_Whisper_Large_V3_Turbo_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Openai_Whisper_Large_V3_Turbo_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Openai_Whisper_Large_V3_Turbo(Base_Ai_Cf_Openai_Whisper_Large_V3_Turbo_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Baai_Bge_M3_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Baai_Bge_M3_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Baai_Bge_M3_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Baai_Bge_M3(Base_Ai_Cf_Baai_Bge_M3_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Black_Forest_Labs_Flux_1_Schnell(Base_Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct(Base_Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast(Base_Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Meta_Llama_Guard_3_8B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Meta_Llama_Guard_3_8B(Base_Ai_Cf_Meta_Llama_Guard_3_8B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Baai_Bge_Reranker_Base_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Baai_Bge_Reranker_Base_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Baai_Bge_Reranker_Base_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Baai_Bge_Reranker_Base(Base_Ai_Cf_Baai_Bge_Reranker_Base_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct(Base_Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Qwen_Qwq_32B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Qwen_Qwq_32B_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Qwen_Qwq_32B_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Qwen_Qwq_32B(Base_Ai_Cf_Qwen_Qwq_32B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct(Base_Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Google_Gemma_3_12B_It_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Google_Gemma_3_12B_It_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Google_Gemma_3_12B_It_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Google_Gemma_3_12B_It(Base_Ai_Cf_Google_Gemma_3_12B_It_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct(Base_Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8(Base_Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Deepgram_Nova_3_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Deepgram_Nova_3_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Deepgram_Nova_3_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Deepgram_Nova_3(Base_Ai_Cf_Deepgram_Nova_3_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Qwen_Qwen3_Embedding_0_6B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Qwen_Qwen3_Embedding_0_6B_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Qwen_Qwen3_Embedding_0_6B_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Qwen_Qwen3_Embedding_0_6B(Base_Ai_Cf_Qwen_Qwen3_Embedding_0_6B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Pipecat_Ai_Smart_Turn_V2_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Pipecat_Ai_Smart_Turn_V2(Base_Ai_Cf_Pipecat_Ai_Smart_Turn_V2_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Openai_Gpt_Oss_120B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: ResponsesInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: ResponsesOutput = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Openai_Gpt_Oss_120B(Base_Ai_Cf_Openai_Gpt_Oss_120B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Openai_Gpt_Oss_20B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: ResponsesInput = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: ResponsesOutput = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Openai_Gpt_Oss_20B(Base_Ai_Cf_Openai_Gpt_Oss_20B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Leonardo_Phoenix_1_0_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Leonardo_Phoenix_1_0_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Leonardo_Phoenix_1_0_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Leonardo_Phoenix_1_0(Base_Ai_Cf_Leonardo_Phoenix_1_0_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Leonardo_Lucid_Origin_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Leonardo_Lucid_Origin_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Leonardo_Lucid_Origin_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Leonardo_Lucid_Origin(Base_Ai_Cf_Leonardo_Lucid_Origin_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Deepgram_Aura_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Deepgram_Aura_1_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Deepgram_Aura_1_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Deepgram_Aura_1(Base_Ai_Cf_Deepgram_Aura_1_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B(Base_Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Input = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It(Base_Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Pfnet_Plamo_Embedding_1B_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Pfnet_Plamo_Embedding_1B_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Pfnet_Plamo_Embedding_1B_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Pfnet_Plamo_Embedding_1B(Base_Ai_Cf_Pfnet_Plamo_Embedding_1B_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Deepgram_Flux_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Deepgram_Flux_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Deepgram_Flux_Output_iface = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Deepgram_Flux(Base_Ai_Cf_Deepgram_Flux_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Deepgram_Aura_2_En_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Deepgram_Aura_2_En_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Deepgram_Aura_2_En_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Deepgram_Aura_2_En(Base_Ai_Cf_Deepgram_Aura_2_En_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Base_Ai_Cf_Deepgram_Aura_2_Es_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: Ai_Cf_Deepgram_Aura_2_Es_Input_iface = ... # type:ignore[assignment,unused-ignore]
    postProcessedOutputs: Ai_Cf_Deepgram_Aura_2_Es_Output = ... # type:ignore[assignment,unused-ignore]

class Base_Ai_Cf_Deepgram_Aura_2_Es(Base_Ai_Cf_Deepgram_Aura_2_Es_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Ai_iface[AiModelList=AiModels_iface](Protocol): # type:ignore[misc, unused-ignore]
    aiGatewayLogId: str | None = ... # type:ignore[assignment,unused-ignore]
    def gateway(self, gatewayId: str, /) -> AiGateway: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def autorag(self, autoragId: str, /) -> AutoRAG: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def run[Name, Options, InputOptions](self, model: Name, inputs: InputOptions, options: Options | None = None, /) -> Future[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def models(self, params: AiModelsSearchParams | None = None, /) -> Future[JsArray[AiModelsSearchObject]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toMarkdown(self, /) -> ToMarkdownService: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toMarkdown(self, files: PyMutableSequence[MarkdownDocument], options: ConversionRequestOptions | None = None, /) -> Future[JsArray[ConversionResponse]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toMarkdown(self, files: MarkdownDocument, options: ConversionRequestOptions | None = None, /) -> Future[ConversionResponse]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Ai[AiModelList=AiModels_iface](Ai_iface[AiModelList], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class AiGateway_iface(Protocol): # type:ignore[misc, unused-ignore]
    def patchLog(self, logId: str, data: AiGatewayPatchLog, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getLog(self, logId: str, /) -> Future[AiGatewayLog]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def run(self, data: AIGatewayUniversalRequest | PyMutableSequence[AIGatewayUniversalRequest], /, *, gateway: UniversalGatewayOptions | None = None, extraHeaders: Any | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUrl(self, provider: AIGatewayProviders | str | None = None, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AiGateway(AiGateway_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class AutoRAG_iface(Protocol): # type:ignore[misc, unused-ignore]
    def list(self, /) -> Future[AutoRagListResponse]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def search(self, params: AutoRagSearchRequest, /) -> Future[AutoRagSearchResponse]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def aiSearch(self, params: AutoRagAiSearchRequestStreaming, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def aiSearch(self, params: AutoRagAiSearchRequest, /) -> Future[AutoRagAiSearchResponse | Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AutoRAG(AutoRAG_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class D1Database_iface(Protocol): # type:ignore[misc, unused-ignore]
    def prepare(self, query: str, /) -> D1PreparedStatement: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def batch[T=Any](self, statements: PyMutableSequence[D1PreparedStatement], /) -> Future[JsArray[D1Result[T]]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def exec(self, query: str, /) -> Future[D1ExecResult_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def withSession(self, constraintOrBookmark: D1SessionBookmark | D1SessionConstraint | None = None, /) -> D1DatabaseSession: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def dump(self, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class D1Database(D1Database_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class D1DatabaseSession_iface(Protocol): # type:ignore[misc, unused-ignore]
    def prepare(self, query: str, /) -> D1PreparedStatement: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def batch[T=Any](self, statements: PyMutableSequence[D1PreparedStatement], /) -> Future[JsArray[D1Result[T]]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getBookmark(self, /) -> D1SessionBookmark | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class D1DatabaseSession(D1DatabaseSession_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class D1PreparedStatement_iface(Protocol): # type:ignore[misc, unused-ignore]
    def bind(self, /, *values: Any) -> D1PreparedStatement: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def first[T=Any](self, colName: str, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def first[T=Record[str, Any]](self, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def run[T=Record[str, Any]](self, /) -> Future[D1Result[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def all[T=Record[str, Any]](self, /) -> Future[D1Result[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def raw[T=JsArray[Any]](self, /, *, columnNames: Literal[True]) -> Future[tuple[JsArray[str], Any]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def raw[T=JsArray[Any]](self, /, *, columnNames: Literal[False] | None = None) -> Future[JsArray[T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class D1PreparedStatement(D1PreparedStatement_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class EmailEvent_iface(ExtendableEvent_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def message(self, /) -> ForwardableEmailMessage_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EmailEvent(EmailEvent_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class ToMarkdownService_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def transform(self, files: PyMutableSequence[MarkdownDocument], options: ConversionRequestOptions | None = None, /) -> Future[JsArray[ConversionResponse]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def transform(self, files: MarkdownDocument, options: ConversionRequestOptions | None = None, /) -> Future[ConversionResponse]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def supported(self, /) -> Future[JsArray[SupportedFileFormat]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ToMarkdownService(ToMarkdownService_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class VectorizeIndex_iface(Protocol): # type:ignore[misc, unused-ignore]
    def describe(self, /) -> Future[VectorizeIndexDetails_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def query(self, vector: VectorFloatArray | PyMutableSequence[int | float], options: VectorizeQueryOptions_iface | None = None, /) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def query(self, vector: VectorFloatArray | PyMutableSequence[int | float], /, *, topK: int | float | None = None, namespace: str | None = None, returnValues: bool | None = None, returnMetadata: bool | VectorizeMetadataRetrievalLevel | None = None, filter: VectorizeVectorMetadataFilter | None = None) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def insert(self, vectors: PyMutableSequence[VectorizeVector_iface], /) -> Future[VectorizeVectorMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def upsert(self, vectors: PyMutableSequence[VectorizeVector_iface], /) -> Future[VectorizeVectorMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deleteByIds(self, ids: PyMutableSequence[str], /) -> Future[VectorizeVectorMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getByIds(self, ids: PyMutableSequence[str], /) -> Future[JsArray[VectorizeVector_iface]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class VectorizeIndex(VectorizeIndex_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Vectorize_iface(Protocol): # type:ignore[misc, unused-ignore]
    def describe(self, /) -> Future[VectorizeIndexInfo_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def query(self, vector: VectorFloatArray | PyMutableSequence[int | float], options: VectorizeQueryOptions_iface | None = None, /) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def query(self, vector: VectorFloatArray | PyMutableSequence[int | float], /, *, topK: int | float | None = None, namespace: str | None = None, returnValues: bool | None = None, returnMetadata: bool | VectorizeMetadataRetrievalLevel | None = None, filter: VectorizeVectorMetadataFilter | None = None) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def queryById(self, vectorId: str, options: VectorizeQueryOptions_iface | None = None, /) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def queryById(self, vectorId: str, /, *, topK: int | float | None = None, namespace: str | None = None, returnValues: bool | None = None, returnMetadata: bool | VectorizeMetadataRetrievalLevel | None = None, filter: VectorizeVectorMetadataFilter | None = None) -> Future[VectorizeMatches_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def insert(self, vectors: PyMutableSequence[VectorizeVector_iface], /) -> Future[VectorizeAsyncMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def upsert(self, vectors: PyMutableSequence[VectorizeVector_iface], /) -> Future[VectorizeAsyncMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deleteByIds(self, ids: PyMutableSequence[str], /) -> Future[VectorizeAsyncMutation_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getByIds(self, ids: PyMutableSequence[str], /) -> Future[JsArray[VectorizeVector_iface]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Vectorize(Vectorize_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class Workflow_iface[PARAMS=Any](Protocol): # type:ignore[misc, unused-ignore]
    def get(self, id: str, /) -> Future[WorkflowInstance]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def create(self, options: WorkflowInstanceCreateOptions_iface[PARAMS] | None = None, /) -> Future[WorkflowInstance]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def create(self, /, *, id: str | None = None, params: PARAMS | None = None, retention: Workflow__create__Sig0 | None = None) -> Future[WorkflowInstance]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def createBatch(self, batch: PyMutableSequence[WorkflowInstanceCreateOptions_iface[PARAMS]], /) -> Future[JsArray[WorkflowInstance]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, id: str, /) -> Future[WorkflowInstance]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Workflow[PARAMS=Any](Workflow_iface[PARAMS], _JsObject): # type:ignore[misc, unused-ignore]
    pass

class WorkflowInstance_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    def pause(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def resume(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def terminate(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def restart(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def status(self, /) -> Future[InstanceStatus]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sendEvent(self, /, *, type: str, payload: Any) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WorkflowInstance(WorkflowInstance_iface, _JsObject): # type:ignore[misc, unused-ignore]
    pass

class DurableObjectId_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def name(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def equals(self, other: DurableObjectId_iface, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def equals(self, /, *, name: str | None = None) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectStorage_iface(Protocol): # type:ignore[misc, unused-ignore]
    sql: SqlStorage_iface = ... # type:ignore[assignment,unused-ignore]
    kv: SyncKvStorage_iface = ... # type:ignore[assignment,unused-ignore]
    @overload
    def get[T=Any](self, key: str, options: DurableObjectGetOptions_iface | None = None, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, key: str, /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, keys: PyMutableSequence[str], options: DurableObjectGetOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, options: DurableObjectListOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, /, *, start: str | None = None, startAfter: str | None = None, end: str | None = None, prefix: str | None = None, reverse: bool | None = None, limit: int | float | None = None, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, key: str, value: T, options: DurableObjectPutOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, key: str, value: T, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, entries: Record[str, T], options: DurableObjectPutOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, entries: Record[str, T], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, key: str, options: DurableObjectPutOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, key: str, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, keys: PyMutableSequence[str], options: DurableObjectPutOptions_iface | None = None, /) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAll(self, options: DurableObjectPutOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAll(self, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def transaction[T](self, closure: DurableObjectStorage_iface__transaction__Sig0__closure[T], /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getAlarm(self, options: DurableObjectGetAlarmOptions_iface | None = None, /) -> Future[int | float | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getAlarm(self, /, *, allowConcurrency: bool | None = None) -> Future[int | float | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setAlarm(self, scheduledTime: int | float | Date, options: DurableObjectSetAlarmOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setAlarm(self, scheduledTime: int | float | Date, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAlarm(self, options: DurableObjectSetAlarmOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAlarm(self, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sync(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def transactionSync[T](self, closure: Callable[[], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getCurrentBookmark(self, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getBookmarkForTime(self, timestamp: int | float | Date, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def onNextSessionRestoreBookmark(self, bookmark: str, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, key: str, options: DurableObjectGetOptions_iface | None = None, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, key: str, /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, keys: PyMutableSequence[str], options: DurableObjectGetOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, key: str, options: DurableObjectPutOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, key: str, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, keys: PyMutableSequence[str], options: DurableObjectPutOptions_iface | None = None, /) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Container_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def start(self, options: ContainerStartupOptions_iface | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def start(self, /, *, entrypoint: PyMutableSequence[str] | None = None, enableInternet: bool, env: Record[str, str] | None = None, hardTimeout: (int | float | int) | None = None) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def monitor(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def destroy(self, error: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def signal(self, signo: int | float, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getTcpPort(self, port: int | float, /) -> Fetcher[None, Never]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setInactivityTimeout(self, durationMs: int | float | int, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class StructuredSerializeOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    transfer: JsArray[Any] | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfProperties_iface(Protocol): # type:ignore[misc, unused-ignore]
    cacheEverything: bool | None = ... # type:ignore[assignment,unused-ignore]
    cacheKey: str | None = ... # type:ignore[assignment,unused-ignore]
    cacheTags: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    cacheTtl: int | float | None = ... # type:ignore[assignment,unused-ignore]
    cacheTtlByStatus: Record[str, int | float] | None = ... # type:ignore[assignment,unused-ignore]
    scrapeShield: bool | None = ... # type:ignore[assignment,unused-ignore]
    apps: bool | None = ... # type:ignore[assignment,unused-ignore]
    image: RequestInitCfPropertiesImage_iface | None = ... # type:ignore[assignment,unused-ignore]
    minify: RequestInitCfPropertiesImageMinify_iface | None = ... # type:ignore[assignment,unused-ignore]
    mirage: bool | None = ... # type:ignore[assignment,unused-ignore]
    polish: Literal["lossy", "lossless", "off"] | None = ... # type:ignore[assignment,unused-ignore]
    r2: RequestInitCfPropertiesR2_iface | None = ... # type:ignore[assignment,unused-ignore]
    resolveOverride: str | None = ... # type:ignore[assignment,unused-ignore]
    def __getattr__(self, key: str, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RequestInit_iface[Cf=CfProperties[Any]](Protocol): # type:ignore[misc, unused-ignore]
    method: str | None = ... # type:ignore[assignment,unused-ignore]
    headers: HeadersInit | None = ... # type:ignore[assignment,unused-ignore]
    body: BodyInit | None = ... # type:ignore[assignment,unused-ignore]
    redirect: str | None = ... # type:ignore[assignment,unused-ignore]
    fetcher: (Fetcher[None, Never] | None) | None = ... # type:ignore[assignment,unused-ignore]
    cf: Cf | None = ... # type:ignore[assignment,unused-ignore]
    cache: Literal["no-store", "no-cache"] | None = ... # type:ignore[assignment,unused-ignore]
    integrity: str | None = ... # type:ignore[assignment,unused-ignore]
    signal: (AbortSignal | None) | None = ... # type:ignore[assignment,unused-ignore]
    encodeResponseBody: Literal["automatic", "manual"] | None = ... # type:ignore[assignment,unused-ignore]

class ServiceWorkerGlobalScope_iface(WorkerGlobalScope_iface, Protocol): # type:ignore[misc, unused-ignore]
    DOMException: Any = ... # type:ignore[assignment,unused-ignore]
    WorkerGlobalScope: Any = ... # type:ignore[assignment,unused-ignore]
    self: ServiceWorkerGlobalScope_iface = ... # type:ignore[assignment,unused-ignore]
    crypto: Crypto = ... # type:ignore[assignment,unused-ignore]
    caches: CacheStorage = ... # type:ignore[assignment,unused-ignore]
    scheduler: Scheduler_iface = ... # type:ignore[assignment,unused-ignore]
    performance: Performance = ... # type:ignore[assignment,unused-ignore]
    Cloudflare: Cloudflare = ... # type:ignore[assignment,unused-ignore]
    @property
    def origin(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    Event: Any = ... # type:ignore[assignment,unused-ignore]
    ExtendableEvent: Any = ... # type:ignore[assignment,unused-ignore]
    CustomEvent: Any = ... # type:ignore[assignment,unused-ignore]
    PromiseRejectionEvent: Any = ... # type:ignore[assignment,unused-ignore]
    FetchEvent: Any = ... # type:ignore[assignment,unused-ignore]
    TailEvent: Any = ... # type:ignore[assignment,unused-ignore]
    TraceEvent: Any = ... # type:ignore[assignment,unused-ignore]
    ScheduledEvent: Any = ... # type:ignore[assignment,unused-ignore]
    MessageEvent: Any = ... # type:ignore[assignment,unused-ignore]
    CloseEvent: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamDefaultReader: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamBYOBReader: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableStream: Any = ... # type:ignore[assignment,unused-ignore]
    WritableStream: Any = ... # type:ignore[assignment,unused-ignore]
    WritableStreamDefaultWriter: Any = ... # type:ignore[assignment,unused-ignore]
    TransformStream: Any = ... # type:ignore[assignment,unused-ignore]
    ByteLengthQueuingStrategy: Any = ... # type:ignore[assignment,unused-ignore]
    CountQueuingStrategy: Any = ... # type:ignore[assignment,unused-ignore]
    ErrorEvent: Any = ... # type:ignore[assignment,unused-ignore]
    MessageChannel: Any = ... # type:ignore[assignment,unused-ignore]
    MessagePort: Any = ... # type:ignore[assignment,unused-ignore]
    EventSource: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamBYOBRequest: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableStreamDefaultController: Any = ... # type:ignore[assignment,unused-ignore]
    ReadableByteStreamController: Any = ... # type:ignore[assignment,unused-ignore]
    WritableStreamDefaultController: Any = ... # type:ignore[assignment,unused-ignore]
    TransformStreamDefaultController: Any = ... # type:ignore[assignment,unused-ignore]
    CompressionStream: Any = ... # type:ignore[assignment,unused-ignore]
    DecompressionStream: Any = ... # type:ignore[assignment,unused-ignore]
    TextEncoderStream: Any = ... # type:ignore[assignment,unused-ignore]
    TextDecoderStream: Any = ... # type:ignore[assignment,unused-ignore]
    Headers: Any = ... # type:ignore[assignment,unused-ignore]
    Body: Any = ... # type:ignore[assignment,unused-ignore]
    Request: Any = ... # type:ignore[assignment,unused-ignore]
    Response: Any = ... # type:ignore[assignment,unused-ignore]
    WebSocket: Any = ... # type:ignore[assignment,unused-ignore]
    WebSocketPair: Any = ... # type:ignore[assignment,unused-ignore]
    WebSocketRequestResponsePair: Any = ... # type:ignore[assignment,unused-ignore]
    AbortController: Any = ... # type:ignore[assignment,unused-ignore]
    AbortSignal: Any = ... # type:ignore[assignment,unused-ignore]
    TextDecoder: Any = ... # type:ignore[assignment,unused-ignore]
    TextEncoder: Any = ... # type:ignore[assignment,unused-ignore]
    navigator: Navigator = ... # type:ignore[assignment,unused-ignore]
    Navigator: Any = ... # type:ignore[assignment,unused-ignore]
    URL: Any = ... # type:ignore[assignment,unused-ignore]
    URLSearchParams: Any = ... # type:ignore[assignment,unused-ignore]
    URLPattern: Any = ... # type:ignore[assignment,unused-ignore]
    Blob: Any = ... # type:ignore[assignment,unused-ignore]
    File: Any = ... # type:ignore[assignment,unused-ignore]
    FormData: Any = ... # type:ignore[assignment,unused-ignore]
    Crypto: Any = ... # type:ignore[assignment,unused-ignore]
    SubtleCrypto: Any = ... # type:ignore[assignment,unused-ignore]
    CryptoKey: Any = ... # type:ignore[assignment,unused-ignore]
    CacheStorage: Any = ... # type:ignore[assignment,unused-ignore]
    Cache: Any = ... # type:ignore[assignment,unused-ignore]
    FixedLengthStream: Any = ... # type:ignore[assignment,unused-ignore]
    IdentityTransformStream: Any = ... # type:ignore[assignment,unused-ignore]
    HTMLRewriter: Any = ... # type:ignore[assignment,unused-ignore]
    def btoa(self, data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def atob(self, data: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setTimeout(self, callback: ServiceWorkerGlobalScope_iface__setTimeout__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setTimeout[*Args](self, callback: ServiceWorkerGlobalScope_iface__setTimeout__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def clearTimeout(self, timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setInterval(self, callback: ServiceWorkerGlobalScope_iface__setInterval__Sig0__callback, msDelay: int | float | None = None, /) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setInterval[*Args](self, callback: ServiceWorkerGlobalScope_iface__setInterval__Sig1__callback[*Args], msDelay: int | float | None = None, /, *args: *Args) -> int | JsProxy: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def clearInterval(self, timeoutId: int | JsProxy, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def queueMicrotask(self, task: Callable[..., Any], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def structuredClone[T](self, value: T, options: StructuredSerializeOptions_iface | None = None, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def structuredClone[T](self, value: T, /, *, transfer: PyMutableSequence[Any] | None = None) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reportError(self, error: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, init: RequestInit_iface[RequestInitCfProperties_iface] | None = None, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: RequestInitCfProperties_iface | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Scheduler_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def wait(self, delay: int | float, maybeOptions: SchedulerWaitOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def wait(self, delay: int | float, /, *, signal: AbortSignal | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SchedulerWaitOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    signal: AbortSignal | None = ... # type:ignore[assignment,unused-ignore]

class Response_iface(Body_iface, Protocol): # type:ignore[misc, unused-ignore]
    status: int = ... # type:ignore[assignment,unused-ignore]
    statusText: str = ... # type:ignore[assignment,unused-ignore]
    headers: Headers = ... # type:ignore[assignment,unused-ignore]
    ok: bool = ... # type:ignore[assignment,unused-ignore]
    redirected: bool = ... # type:ignore[assignment,unused-ignore]
    url: str = ... # type:ignore[assignment,unused-ignore]
    webSocket: WebSocket | None = ... # type:ignore[assignment,unused-ignore]
    cf: Any | None = ... # type:ignore[assignment,unused-ignore]
    Literal["default", "error"]
    def clone(self, /) -> Response: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ResponseInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    status: int | float | None = ... # type:ignore[assignment,unused-ignore]
    statusText: str | None = ... # type:ignore[assignment,unused-ignore]
    headers: HeadersInit | None = ... # type:ignore[assignment,unused-ignore]
    cf: Any | None = ... # type:ignore[assignment,unused-ignore]
    webSocket: (WebSocket | None) | None = ... # type:ignore[assignment,unused-ignore]
    encodeBody: Literal["automatic", "manual"] | None = ... # type:ignore[assignment,unused-ignore]

class Request_iface[CfHostMetadata=Any, Cf=Any](Body_iface, Protocol): # type:ignore[misc, unused-ignore]
    method: str = ... # type:ignore[assignment,unused-ignore]
    url: str = ... # type:ignore[assignment,unused-ignore]
    headers: Headers = ... # type:ignore[assignment,unused-ignore]
    redirect: str = ... # type:ignore[assignment,unused-ignore]
    fetcher: Fetcher[None, Never] | None = ... # type:ignore[assignment,unused-ignore]
    signal: AbortSignal = ... # type:ignore[assignment,unused-ignore]
    cf: Cf | None = ... # type:ignore[assignment,unused-ignore]
    integrity: str = ... # type:ignore[assignment,unused-ignore]
    keepalive: bool = ... # type:ignore[assignment,unused-ignore]
    cache: Literal["no-store", "no-cache"] | None = ... # type:ignore[assignment,unused-ignore]
    def clone(self, /) -> Request[CfHostMetadata, Cf]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStream_iface[R=Any](Protocol): # type:ignore[misc, unused-ignore]
    def cancel(self, reason: Any | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getReader(self, /) -> ReadableStreamDefaultReader[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getReader(self, options: ReadableStreamGetReaderOptions_iface, /) -> ReadableStreamBYOBReader: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getReader(self, /, *, mode: Literal["byob"]) -> ReadableStreamBYOBReader: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def pipeThrough[T](self, transform: ReadableWritablePair_iface[T, R], options: StreamPipeOptions_iface | None = None, /) -> ReadableStream[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def pipeThrough[T](self, transform: ReadableWritablePair_iface[T, R], /, *, preventClose: bool | None = None, preventAbort: bool | None = None, preventCancel: bool | None = None, signal: AbortSignal | None = None) -> ReadableStream[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def pipeTo(self, destination: WritableStream[R], options: StreamPipeOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def pipeTo(self, destination: WritableStream[R], /, *, preventClose: bool | None = None, preventAbort: bool | None = None, preventCancel: bool | None = None, signal: AbortSignal | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def tee(self, /) -> tuple[ReadableStream[R], ReadableStream[R]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def values(self, options: ReadableStreamValuesOptions_iface | None = None, /) -> JsAsyncIterator[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def values(self, /, *, preventCancel: bool | None = None) -> JsAsyncIterator[R]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class UnderlyingByteSource_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["bytes"] = ... # type:ignore[assignment,unused-ignore]
    autoAllocateChunkSize: int | float | None = ... # type:ignore[assignment,unused-ignore]
    start: Callable[[ReadableByteStreamController], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    pull: Callable[[ReadableByteStreamController], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    cancel: Callable[[Any], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]

class QueuingStrategy_iface[T=Any](Protocol): # type:ignore[misc, unused-ignore]
    highWaterMark: (int | float | int) | None = ... # type:ignore[assignment,unused-ignore]
    size: Callable[[T], int | float | int] | None = ... # type:ignore[assignment,unused-ignore]

class UnderlyingSource_iface[R=Any](Protocol): # type:ignore[misc, unused-ignore]
    type: None | Literal[""] | None = ... # type:ignore[assignment,unused-ignore]
    start: Callable[[ReadableStreamDefaultController[R]], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    pull: Callable[[ReadableStreamDefaultController[R]], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    cancel: Callable[[Any], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    expectedLength: (int | float | int) | None = ... # type:ignore[assignment,unused-ignore]

class WebSocket_iface(EventTarget_iface[WebSocketEventMap], Protocol): # type:ignore[misc, unused-ignore]
    readyState: int | float = ... # type:ignore[assignment,unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]
    protocol: str | None = ... # type:ignore[assignment,unused-ignore]
    extensions: str | None = ... # type:ignore[assignment,unused-ignore]
    def accept(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def send(self, message: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def close(self, code: int | float | None = None, reason: str | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def serializeAttachment(self, attachment: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deserializeAttachment(self, /) -> Any | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Object_iface(Protocol): # type:ignore[misc, unused-ignore]
    constructor: Callable[..., Any] = ... # type:ignore[assignment,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Object: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def hasOwnProperty(self, v: PropertyKey, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def isPrototypeOf(self, v: Object, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def propertyIsEnumerable(self, v: PropertyKey, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class PropertyDescriptor_iface(Protocol): # type:ignore[misc, unused-ignore]
    configurable: bool | None = ... # type:ignore[assignment,unused-ignore]
    enumerable: bool | None = ... # type:ignore[assignment,unused-ignore]
    value: Any | None = ... # type:ignore[assignment,unused-ignore]
    writable: bool | None = ... # type:ignore[assignment,unused-ignore]
    def get(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, v: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, v: Any, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class PropertyDescriptorMap_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ThisType_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    pass

class Function_iface(Protocol): # type:ignore[misc, unused-ignore]
    prototype: Any = ... # type:ignore[assignment,unused-ignore]
    @property
    def length(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    arguments: Any = ... # type:ignore[assignment,unused-ignore]
    caller: Callable[..., Any] = ... # type:ignore[assignment,unused-ignore]
    @property
    def name(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def apply(self, this: Callable[..., Any], thisArg: Any, argArray: Any | None = None, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def call(self, this: Callable[..., Any], thisArg: Any, /, *argArray: Any) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def bind(self, this: Callable[..., Any], thisArg: Any, /, *argArray: Any) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class String_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def length(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def charAt(self, pos: int | float, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def charCodeAt(self, index: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def concat(self, /, *strings: str) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchString: str, position: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchString: str, position: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def localeCompare(self, that: str, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def localeCompare(self, that: str, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def localeCompare(self, that: str, locales: Any | None = None, options: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def match(self, regexp: str | RegExp, /) -> RegExpMatchArray_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def match(self, /) -> RegExpMatchArray_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, searchValue: str | RegExp, replaceValue: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, searchValue: str | RegExp, replacer: String_iface__replace__Sig1__replacer, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, searchValue: String_iface__replace__Sig2__searchValue, replaceValue: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, searchValue: String_iface__replace__Sig3__searchValue, replacer: String_iface__replace__Sig3__replacer, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def search(self, regexp: str | RegExp, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def search(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | float | None = None, end: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def split(self, separator: str | RegExp, limit: int | float | None = None, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def split(self, splitter: String_iface__split__Sig1__splitter, limit: int | float | None = None, /) -> JsArray[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def substring(self, start: int | float, end: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toLowerCase(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleLowerCase(self, locales: str | PyMutableSequence[str] | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleLowerCase(self, locales: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toUpperCase(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleUpperCase(self, locales: str | PyMutableSequence[str] | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleUpperCase(self, locales: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def trim(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def substr(self, from_: int | float, length: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def codePointAt(self, pos: int | float, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchString: str, position: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def endsWith(self, searchString: str, endPosition: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def normalize(self, form: Literal["NFC", "NFD", "NFKC", "NFKD"], /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def normalize(self, form: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def repeat(self, count: int | float, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def startsWith(self, searchString: str, position: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def anchor(self, name: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def big(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def blink(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def bold(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fixed(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fontcolor(self, color: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fontsize(self, size: int | float, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fontsize(self, size: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def italics(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def link(self, url: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def small(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def strike(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sub(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sup(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def padStart(self, maxLength: int | float, fillString: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def padEnd(self, maxLength: int | float, fillString: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def trimEnd(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def trimStart(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def trimLeft(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def trimRight(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def matchAll(self, regexp: RegExp, /) -> RegExpStringIterator_iface[RegExpExecArray_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replaceAll(self, searchValue: str | RegExp, replaceValue: str, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replaceAll(self, searchValue: str | RegExp, replacer: String_iface__replaceAll__Sig1__replacer, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int | float, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def isWellFormed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toWellFormed(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchString: str, position: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Boolean_iface(Protocol): # type:ignore[misc, unused-ignore]
    def valueOf(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Number_iface(Protocol): # type:ignore[misc, unused-ignore]
    def toString(self, radix: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toFixed(self, fractionDigits: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toExponential(self, fractionDigits: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toPrecision(self, precision: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: Any | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Date_iface(Protocol): # type:ignore[misc, unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toDateString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toTimeString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: Any | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleDateString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleDateString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleDateString(self, locales: Any | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleTimeString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleTimeString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleTimeString(self, locales: Any | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getTime(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getFullYear(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCFullYear(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getMonth(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCMonth(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getDate(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCDate(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getDay(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCDay(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getHours(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCHours(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getMinutes(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCMinutes(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getSeconds(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCSeconds(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getMilliseconds(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUTCMilliseconds(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getTimezoneOffset(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setTime(self, time: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setMilliseconds(self, ms: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCMilliseconds(self, ms: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setSeconds(self, sec: int | float, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCSeconds(self, sec: int | float, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setMinutes(self, min: int | float, sec: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCMinutes(self, min: int | float, sec: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setHours(self, hours: int | float, min: int | float | None = None, sec: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCHours(self, hours: int | float, min: int | float | None = None, sec: int | float | None = None, ms: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setDate(self, date: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCDate(self, date: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setMonth(self, month: int | float, date: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCMonth(self, month: int | float, date: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setFullYear(self, year: int | float, month: int | float | None = None, date: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUTCFullYear(self, year: int | float, month: int | float | None = None, date: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toUTCString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toISOString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toJSON(self, key: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Error_iface(Exception): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    message: str = ... # type:ignore[assignment,unused-ignore]
    stack: str | None = ... # type:ignore[assignment,unused-ignore]
    cause: Any | None = ... # type:ignore[assignment,unused-ignore]

class ErrorOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    cause: Any | None = ... # type:ignore[assignment,unused-ignore]

class EvalError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class RangeError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class ReferenceError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class SyntaxError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class TypeError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class URIError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    pass

class AsyncIterable_iface[T, TReturn=Any, TNext=Any](Protocol): # type:ignore[misc, unused-ignore]
    pass

class ArrayBuffer_iface(JsBuffer): # type:ignore[misc, unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, begin: int | None = None, end: int | None = None, /) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def resize(self, newByteLength: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def transfer(self, newByteLength: int | None = None, /) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def transferToFixedLength(self, newByteLength: int | None = None, /) -> ArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DataView_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getFloat32(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getFloat64(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getInt8(self, byteOffset: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getInt16(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getInt32(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUint8(self, byteOffset: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUint16(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUint32(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setFloat32(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setFloat64(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setInt8(self, byteOffset: int | float, value: int | float, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setInt16(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setInt32(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUint8(self, byteOffset: int | float, value: int | float, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUint16(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setUint32(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getBigInt64(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getBigUint64(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setBigInt64(self, byteOffset: int | float, value: int, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setBigUint64(self, byteOffset: int | float, value: int, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getFloat16(self, byteOffset: int | float, littleEndian: bool | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setFloat16(self, byteOffset: int | float, value: int | float, littleEndian: bool | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int8Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Int8Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Int8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint8Array_iface[TArrayBuffer=ArrayBufferLike](JsBuffer): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Uint8Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Uint8Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint8ClampedArray_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Uint8ClampedArray[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Uint8ClampedArray[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int16Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Int16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Int16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint16Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Uint16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Uint16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Int32Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Int32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Int32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Uint32Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, Self], int], thisArg: Any | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, Self], int], initialValue: int, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> Uint32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> Uint32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float32Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int | float, start: int | float, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int | float, start: int | float | None = None, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int | float, int | float, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int | float, int | float, Self], int | float], thisArg: Any | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | float | None = None, end: int | float | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | float | None = None, end: int | float | None = None, /) -> Float32Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int | float, int | float]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int | float, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int | float, value: int | float, /) -> Float32Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float64Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int | float, start: int | float, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int | float, start: int | float | None = None, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int | float, int | float, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int | float, int | float, Self], int | float], thisArg: Any | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | float | None = None, end: int | float | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | float | None = None, end: int | float | None = None, /) -> Float64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int | float, int | float]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int | float, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int | float, value: int | float, /) -> Float64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WeakMap_iface[K, V](Protocol): # type:ignore[misc, unused-ignore]
    def delete(self, key: K, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def get(self, key: K, /) -> V | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, key: K, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, key: K, value: V, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, key: K, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, key: K, /) -> V | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, key: K, value: V, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, key: K, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Set_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def size(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def add(self, value: T, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def clear(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[T, T, Set[T]], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> SetIterator_iface[tuple[T, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> SetIterator_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> SetIterator_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def union[U](self, other: ReadonlySetLike_iface[U], /) -> Set[T | U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def union[U](self, /, *, size: int | float) -> Set[T | U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def intersection[U](self, other: ReadonlySetLike_iface[U], /) -> Set[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def intersection[U](self, /, *, size: int | float) -> Set[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def difference[U](self, other: ReadonlySetLike_iface[U], /) -> Set[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def difference[U](self, /, *, size: int | float) -> Set[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def symmetricDifference[U](self, other: ReadonlySetLike_iface[U], /) -> Set[T | U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def symmetricDifference[U](self, /, *, size: int | float) -> Set[T | U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isSubsetOf(self, other: ReadonlySetLike_iface[Any], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isSubsetOf(self, /, *, size: int | float) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isSupersetOf(self, other: ReadonlySetLike_iface[Any], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isSupersetOf(self, /, *, size: int | float) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isDisjointFrom(self, other: ReadonlySetLike_iface[Any], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def isDisjointFrom(self, /, *, size: int | float) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WeakSet_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    def add(self, value: T, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Symbol_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def description(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Symbol: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ProxyHandler_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    def apply(self, target: T, thisArg: Any, argArray: PyMutableSequence[Any], /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def construct(self, target: T, argArray: PyMutableSequence[Any], newTarget: Callable[..., Any], /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def defineProperty(self, target: T, property: str | Symbol, attributes: PropertyDescriptor_iface, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def defineProperty(self, target: T, property: str | Symbol, /, *, configurable: bool | None = None, enumerable: bool | None = None, value: Any | None = None, writable: bool | None = None) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def deleteProperty(self, target: T, p: str | Symbol, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def get(self, target: T, p: str | Symbol, receiver: Any, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getOwnPropertyDescriptor(self, target: T, p: str | Symbol, /) -> PropertyDescriptor_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getPrototypeOf(self, target: T, /) -> Any | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, target: T, p: str | Symbol, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def isExtensible(self, target: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def ownKeys(self, target: T, /) -> ArrayLike_iface[str | Symbol]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def preventExtensions(self, target: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, target: T, p: str | Symbol, newValue: Any, receiver: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setPrototypeOf(self, target: T, v: Any | None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, target: T, p: str | Symbol, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__(self, target: T, p: str | Symbol, receiver: Any, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, target: T, p: str | Symbol, newValue: Any, receiver: Any, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SharedArrayBuffer_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, begin: int | None = None, end: int | None = None, /) -> SharedArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def grow(self, newByteLength: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigInt_iface(Protocol): # type:ignore[misc, unused-ignore]
    def toString(self, radix: int | float | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: Any | None = None, options: BigIntToLocaleStringOptions_iface | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: Any | None = None, /, *, localeMatcher: str | None = None, style: str | None = None, numberingSystem: str | None = None, unit: str | None = None, unitDisplay: str | None = None, currency: str | None = None, currencyDisplay: str | None = None, useGrouping: bool | None = None, minimumIntegerDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = None, minimumFractionDigits: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | None = None, maximumFractionDigits: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | None = None, minimumSignificantDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = None, maximumSignificantDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = None, notation: str | None = None, compactDisplay: str | None = None) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigInt64Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, BigInt64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, BigInt64Array[TArrayBuffer]], Any], thisArg: Any | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, BigInt64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, BigInt64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, BigInt64Array[TArrayBuffer]], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, BigInt64Array[TArrayBuffer]], int], thisArg: Any | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, BigInt64Array[TArrayBuffer]], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, BigInt64Array[TArrayBuffer]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, BigInt64Array[TArrayBuffer]], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, BigInt64Array[TArrayBuffer]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, BigInt64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int | int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> BigInt64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toLocaleString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> BigInt64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> BigInt64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigUint64Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, int]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int, int, BigUint64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int, int, BigUint64Array[TArrayBuffer]], Any], thisArg: Any | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int, int, BigUint64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int, int, BigUint64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int, int, BigUint64Array[TArrayBuffer]], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int, int, BigUint64Array[TArrayBuffer]], int], thisArg: Any | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int, int, int, BigUint64Array[TArrayBuffer]], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int, int, BigUint64Array[TArrayBuffer]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int, int, int, BigUint64Array[TArrayBuffer]], int], /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int, int, BigUint64Array[TArrayBuffer]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int, int, BigUint64Array[TArrayBuffer]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int, int], int | int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | None = None, end: int | None = None, /) -> BigUint64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toLocaleString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> BigUint64Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int, int, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int, int, Self], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int, int], int] | None = None, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: int, /) -> BigUint64Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int], offset: int | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AggregateError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    errors: JsArray[Any] = ... # type:ignore[assignment,unused-ignore]

class WeakRef_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    def deref(self, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class FinalizationRegistry_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    def register(self, target: WeakKey, heldValue: T, unregisterToken: WeakKey | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def unregister(self, unregisterToken: WeakKey, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SuppressedError_iface(Error_iface): # type:ignore[misc, unused-ignore]
    error: Any = ... # type:ignore[assignment,unused-ignore]
    suppressed: Any = ... # type:ignore[assignment,unused-ignore]

class DisposableStack_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def disposed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def dispose(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def use[T](self, value: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def adopt[T](self, value: T, onDispose: Callable[[T], None], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def defer(self, onDispose: Callable[[], None], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def move(self, /) -> DisposableStack: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class AsyncDisposableStack_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def disposed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def disposeAsync(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def use[T](self, value: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def adopt[T](self, value: T, onDisposeAsync: Callable[[T], PromiseLike_iface[None] | None], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def defer(self, onDisposeAsync: Callable[[], PromiseLike_iface[None] | None], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def move(self, /) -> AsyncDisposableStack: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Float16Array_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def BYTES_PER_ELEMENT(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def length(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int | float, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int | float, start: int | float, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: int | float, start: int | float | None = None, end: int | float | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def filter(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def find(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[int | float, int | float, Self], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[int | float, int | float, Self], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map(self, callbackfn: Callable[[int | float, int | float, Self], int | float], thisArg: Any | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[int | float, int | float, int | float, Self], int | float], initialValue: int | float, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, int | float, int | float, Self], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def set(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | float | None = None, end: int | float | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[int | float, int | float, Self], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def subarray(self, begin: int | float | None = None, end: int | float | None = None, /) -> Float16Array[TArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toLocaleString(self, locales: str | PyMutableSequence[str] | None = None, options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[int | float, int | float], int | float] | None = None, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def valueOf(self, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int | float, value: int | float, /) -> Float16Array[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int | float, int | float]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: int | float, fromIndex: int | float | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __setitem__(self, array: ArrayLike_iface[int | float], offset: int | float | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class EventTargetAddEventListenerOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    capture: bool | None = ... # type:ignore[assignment,unused-ignore]
    passive: bool | None = ... # type:ignore[assignment,unused-ignore]
    once: bool | None = ... # type:ignore[assignment,unused-ignore]
    signal: AbortSignal | None = ... # type:ignore[assignment,unused-ignore]

class EventTargetEventListenerOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    capture: bool | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectNamespaceGetDurableObjectOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    locationHint: DurableObjectLocationHint | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectNamespaceNewUniqueIdOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    jurisdiction: DurableObjectJurisdiction | None = ... # type:ignore[assignment,unused-ignore]

class EventInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    bubbles: bool | None = ... # type:ignore[assignment,unused-ignore]
    cancelable: bool | None = ... # type:ignore[assignment,unused-ignore]
    composed: bool | None = ... # type:ignore[assignment,unused-ignore]

class CustomEventCustomEventInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    bubbles: bool | None = ... # type:ignore[assignment,unused-ignore]
    cancelable: bool | None = ... # type:ignore[assignment,unused-ignore]
    composed: bool | None = ... # type:ignore[assignment,unused-ignore]
    detail: Any | None = ... # type:ignore[assignment,unused-ignore]

class ArrayBufferView_iface[TArrayBuffer=ArrayBufferLike](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def buffer(self, /) -> TArrayBuffer: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteLength(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def byteOffset(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BlobOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]

class FileOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    lastModified: int | float | None = ... # type:ignore[assignment,unused-ignore]

class CacheQueryOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    ignoreMethod: bool | None = ... # type:ignore[assignment,unused-ignore]

class SubtleCryptoEncryptAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    iv: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    additionalData: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    tagLength: int | float | None = ... # type:ignore[assignment,unused-ignore]
    counter: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    length: int | float | None = ... # type:ignore[assignment,unused-ignore]
    label: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SubtleCryptoSignAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    hash: (str | SubtleCryptoHashAlgorithm_iface) | None = ... # type:ignore[assignment,unused-ignore]
    dataLength: int | float | None = ... # type:ignore[assignment,unused-ignore]
    saltLength: int | float | None = ... # type:ignore[assignment,unused-ignore]

class SubtleCryptoHashAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]

class SubtleCryptoGenerateKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    hash: (str | SubtleCryptoHashAlgorithm_iface) | None = ... # type:ignore[assignment,unused-ignore]
    modulusLength: int | float | None = ... # type:ignore[assignment,unused-ignore]
    publicExponent: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    length: int | float | None = ... # type:ignore[assignment,unused-ignore]
    namedCurve: str | None = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CryptoKeyPair_iface(Protocol): # type:ignore[misc, unused-ignore]
    publicKey: CryptoKey = ... # type:ignore[assignment,unused-ignore]
    privateKey: CryptoKey = ... # type:ignore[assignment,unused-ignore]

class SubtleCryptoDeriveKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    salt: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]
    iterations: int | float | None = ... # type:ignore[assignment,unused-ignore]
    hash: (str | SubtleCryptoHashAlgorithm_iface) | None = ... # type:ignore[assignment,unused-ignore]
    
    info: (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | None = ... # type:ignore[assignment,unused-ignore]

class SubtleCryptoImportKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    hash: (str | SubtleCryptoHashAlgorithm_iface) | None = ... # type:ignore[assignment,unused-ignore]
    length: int | float | None = ... # type:ignore[assignment,unused-ignore]
    namedCurve: str | None = ... # type:ignore[assignment,unused-ignore]
    compressed: bool | None = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class JsonWebKey_iface(Protocol): # type:ignore[misc, unused-ignore]
    kty: str = ... # type:ignore[assignment,unused-ignore]
    use: str | None = ... # type:ignore[assignment,unused-ignore]
    key_ops: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    alg: str | None = ... # type:ignore[assignment,unused-ignore]
    ext: bool | None = ... # type:ignore[assignment,unused-ignore]
    crv: str | None = ... # type:ignore[assignment,unused-ignore]
    x: str | None = ... # type:ignore[assignment,unused-ignore]
    y: str | None = ... # type:ignore[assignment,unused-ignore]
    d: str | None = ... # type:ignore[assignment,unused-ignore]
    n: str | None = ... # type:ignore[assignment,unused-ignore]
    e: str | None = ... # type:ignore[assignment,unused-ignore]
    p: str | None = ... # type:ignore[assignment,unused-ignore]
    q: str | None = ... # type:ignore[assignment,unused-ignore]
    dp: str | None = ... # type:ignore[assignment,unused-ignore]
    dq: str | None = ... # type:ignore[assignment,unused-ignore]
    qi: str | None = ... # type:ignore[assignment,unused-ignore]
    oth: JsArray[RsaOtherPrimesInfo_iface] | None = ... # type:ignore[assignment,unused-ignore]
    k: str | None = ... # type:ignore[assignment,unused-ignore]

class CryptoKeyKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]

class CryptoKeyAesKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    length: int | float = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CryptoKeyHmacKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    hash: CryptoKeyKeyAlgorithm_iface = ... # type:ignore[assignment,unused-ignore]
    length: int | float = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class CryptoKeyRsaKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    modulusLength: int | float = ... # type:ignore[assignment,unused-ignore]
    publicExponent: ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike] = ... # type:ignore[assignment,unused-ignore]
    hash: CryptoKeyKeyAlgorithm_iface | None = ... # type:ignore[assignment,unused-ignore]

class CryptoKeyEllipticKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    namedCurve: str = ... # type:ignore[assignment,unused-ignore]

class CryptoKeyArbitraryKeyAlgorithm_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    hash: CryptoKeyKeyAlgorithm_iface | None = ... # type:ignore[assignment,unused-ignore]
    namedCurve: str | None = ... # type:ignore[assignment,unused-ignore]
    length: int | float | None = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TextDecoderDecodeOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    stream: bool = ... # type:ignore[assignment,unused-ignore]

class TextDecoderConstructorOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    fatal: bool = ... # type:ignore[assignment,unused-ignore]
    ignoreBOM: bool = ... # type:ignore[assignment,unused-ignore]

class TextEncoderEncodeIntoResult_iface(Protocol): # type:ignore[misc, unused-ignore]
    read: int | float = ... # type:ignore[assignment,unused-ignore]
    written: int | float = ... # type:ignore[assignment,unused-ignore]

class ErrorEventErrorEventInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    message: str | None = ... # type:ignore[assignment,unused-ignore]
    filename: str | None = ... # type:ignore[assignment,unused-ignore]
    lineno: int | float | None = ... # type:ignore[assignment,unused-ignore]
    colno: int | float | None = ... # type:ignore[assignment,unused-ignore]
    error: Any | None = ... # type:ignore[assignment,unused-ignore]

class MessageEventInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    data: ArrayBuffer | str = ... # type:ignore[assignment,unused-ignore]

class HTMLRewriterElementContentHandlers_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def element(self, element: Element_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def element(self, /, *, tagName: str, attributes: PyIterator[PyMutableSequence[str]], removed: bool, namespaceURI: str) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def comments(self, comment: Comment_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def comments(self, /, *, text: str, removed: bool) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def text(self, element: Text_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def text(self, /, *, text: str, lastInTextNode: bool, removed: bool) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class HTMLRewriterDocumentContentHandlers_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def doctype(self, doctype: Doctype_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def doctype(self, /, *, name: str | None, publicId: str | None, systemId: str | None) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def comments(self, comment: Comment_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def comments(self, /, *, text: str, removed: bool) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def text(self, text: Text_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def text(self, /, *, text: str, lastInTextNode: bool, removed: bool) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def end(self, end: DocumentEnd_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def end(self, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2GetOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    onlyIf: (R2Conditional_iface | Headers) | None = ... # type:ignore[assignment,unused-ignore]
    range: (R2Range | Headers) | None = ... # type:ignore[assignment,unused-ignore]
    ssecKey: (ArrayBuffer | str) | None = ... # type:ignore[assignment,unused-ignore]

class R2Conditional_iface(Protocol): # type:ignore[misc, unused-ignore]
    etagMatches: str | None = ... # type:ignore[assignment,unused-ignore]
    etagDoesNotMatch: str | None = ... # type:ignore[assignment,unused-ignore]
    uploadedBefore: Date | None = ... # type:ignore[assignment,unused-ignore]
    uploadedAfter: Date | None = ... # type:ignore[assignment,unused-ignore]
    secondsGranularity: bool | None = ... # type:ignore[assignment,unused-ignore]

class R2ObjectBody_iface(R2Object_iface, Protocol): # type:ignore[misc, unused-ignore]
    def arrayBuffer(self, /) -> Future[ArrayBuffer]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def bytes(self, /) -> Future[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def text(self, /) -> Future[str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def json[T](self, /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def blob(self, /) -> Future[Blob]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2PutOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    onlyIf: (R2Conditional_iface | Headers) | None = ... # type:ignore[assignment,unused-ignore]
    httpMetadata: (R2HTTPMetadata_iface | Headers) | None = ... # type:ignore[assignment,unused-ignore]
    customMetadata: Record[str, str] | None = ... # type:ignore[assignment,unused-ignore]
    md5: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = ... # type:ignore[assignment,unused-ignore]
    sha1: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = ... # type:ignore[assignment,unused-ignore]
    sha256: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = ... # type:ignore[assignment,unused-ignore]
    sha384: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = ... # type:ignore[assignment,unused-ignore]
    sha512: ((ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str) | None = ... # type:ignore[assignment,unused-ignore]
    storageClass: str | None = ... # type:ignore[assignment,unused-ignore]
    ssecKey: (ArrayBuffer | str) | None = ... # type:ignore[assignment,unused-ignore]

class R2HTTPMetadata_iface(Protocol): # type:ignore[misc, unused-ignore]
    contentType: str | None = ... # type:ignore[assignment,unused-ignore]
    contentLanguage: str | None = ... # type:ignore[assignment,unused-ignore]
    contentDisposition: str | None = ... # type:ignore[assignment,unused-ignore]
    contentEncoding: str | None = ... # type:ignore[assignment,unused-ignore]
    cacheControl: str | None = ... # type:ignore[assignment,unused-ignore]
    cacheExpiry: Date | None = ... # type:ignore[assignment,unused-ignore]

class R2MultipartOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    httpMetadata: (R2HTTPMetadata_iface | Headers) | None = ... # type:ignore[assignment,unused-ignore]
    customMetadata: Record[str, str] | None = ... # type:ignore[assignment,unused-ignore]
    storageClass: str | None = ... # type:ignore[assignment,unused-ignore]
    ssecKey: (ArrayBuffer | str) | None = ... # type:ignore[assignment,unused-ignore]

class R2MultipartUpload_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def key(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def uploadId(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def uploadPart(self, partNumber: int | float, value: ReadableStream[Any] | (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob, options: R2UploadPartOptions_iface | None = None, /) -> Future[R2UploadedPart_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def uploadPart(self, partNumber: int | float, value: ReadableStream[Any] | (ArrayBuffer | ArrayBufferView_iface[ArrayBufferLike]) | str | Blob, /, *, ssecKey: (ArrayBuffer | str) | None = None) -> Future[R2UploadedPart_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def abort(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def complete(self, uploadedParts: PyMutableSequence[R2UploadedPart_iface], /) -> Future[R2Object]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2ListOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    limit: int | float | None = ... # type:ignore[assignment,unused-ignore]
    prefix: str | None = ... # type:ignore[assignment,unused-ignore]
    cursor: str | None = ... # type:ignore[assignment,unused-ignore]
    delimiter: str | None = ... # type:ignore[assignment,unused-ignore]
    startAfter: str | None = ... # type:ignore[assignment,unused-ignore]
    include: JsArray[(Literal["httpMetadata", "customMetadata"])] | None = ... # type:ignore[assignment,unused-ignore]

class R2Checksums_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def md5(self, /) -> ArrayBuffer | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def sha1(self, /) -> ArrayBuffer | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def sha256(self, /) -> ArrayBuffer | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def sha384(self, /) -> ArrayBuffer | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def sha512(self, /) -> ArrayBuffer | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toJSON(self, /) -> R2StringChecksums_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class UnderlyingSink_iface[W=Any](Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    start: Callable[[WritableStreamDefaultController], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    write: Callable[[W, WritableStreamDefaultController], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    abort: Callable[[Any], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    close: Callable[[], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]

class Transformer_iface[I=Any, O=Any](Protocol): # type:ignore[misc, unused-ignore]
    readableType: str | None = ... # type:ignore[assignment,unused-ignore]
    writableType: str | None = ... # type:ignore[assignment,unused-ignore]
    start: Callable[[TransformStreamDefaultController[O]], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    transform: Callable[[I, TransformStreamDefaultController[O]], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    flush: Callable[[TransformStreamDefaultController[O]], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    cancel: Callable[[Any], None | Future[None]] | None = ... # type:ignore[assignment,unused-ignore]
    expectedLength: int | float | None = ... # type:ignore[assignment,unused-ignore]

class IdentityTransformStreamQueuingStrategy_iface(Protocol): # type:ignore[misc, unused-ignore]
    highWaterMark: (int | float | int) | None = ... # type:ignore[assignment,unused-ignore]

class TextDecoderStreamTextDecoderStreamInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    fatal: bool | None = ... # type:ignore[assignment,unused-ignore]
    ignoreBOM: bool | None = ... # type:ignore[assignment,unused-ignore]

class QueuingStrategyInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    highWaterMark: int | float = ... # type:ignore[assignment,unused-ignore]

class TraceItem_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def event(self, /) -> (TraceItemFetchEventInfo_iface | TraceItemJsRpcEventInfo_iface | TraceItemScheduledEventInfo_iface | TraceItemAlarmEventInfo_iface | TraceItemQueueEventInfo_iface | TraceItemEmailEventInfo_iface | TraceItemTailEventInfo_iface | TraceItemCustomEventInfo_iface | TraceItemHibernatableWebSocketEventInfo_iface) | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def eventTimestamp(self, /) -> int | float | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def logs(self, /) -> JsArray[TraceLog_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def exceptions(self, /) -> JsArray[TraceException_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def diagnosticsChannelEvents(self, /) -> JsArray[TraceDiagnosticChannelEvent_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def scriptName(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def entrypoint(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def scriptVersion(self, /) -> ScriptVersion_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def dispatchNamespace(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def scriptTags(self, /) -> JsArray[str] | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def durableObjectId(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def outcome(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def executionModel(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def truncated(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def cpuTime(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def wallTime(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class URLPatternInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    protocol: str | None = ... # type:ignore[assignment,unused-ignore]
    username: str | None = ... # type:ignore[assignment,unused-ignore]
    password: str | None = ... # type:ignore[assignment,unused-ignore]
    hostname: str | None = ... # type:ignore[assignment,unused-ignore]
    port: str | None = ... # type:ignore[assignment,unused-ignore]
    pathname: str | None = ... # type:ignore[assignment,unused-ignore]
    search: str | None = ... # type:ignore[assignment,unused-ignore]
    hash: str | None = ... # type:ignore[assignment,unused-ignore]
    baseURL: str | None = ... # type:ignore[assignment,unused-ignore]

class URLPatternResult_iface(Protocol): # type:ignore[misc, unused-ignore]
    inputs: JsArray[(str | URLPatternInit_iface)] = ... # type:ignore[assignment,unused-ignore]
    protocol: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    username: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    password: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    hostname: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    port: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    pathname: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    search: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]
    hash: URLPatternComponentResult_iface = ... # type:ignore[assignment,unused-ignore]

class URLPatternOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    ignoreCase: bool | None = ... # type:ignore[assignment,unused-ignore]

class CloseEventInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    code: int | float | None = ... # type:ignore[assignment,unused-ignore]
    reason: str | None = ... # type:ignore[assignment,unused-ignore]
    wasClean: bool | None = ... # type:ignore[assignment,unused-ignore]

class EventSourceEventSourceInit_iface(Protocol): # type:ignore[misc, unused-ignore]
    withCredentials: bool | None = ... # type:ignore[assignment,unused-ignore]
    fetcher: Fetcher[None, Never] | None = ... # type:ignore[assignment,unused-ignore]

class MessagePortPostMessageOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    transfer: JsArray[Any] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    word_count: int | float | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[Ai_Cf_Openai_Whisper_Output_iface__words__array] | None = ... # type:ignore[assignment,unused-ignore]
    vtt: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    description: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Tiny_En_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    word_count: int | float | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[Ai_Cf_Openai_Whisper_Tiny_En_Output_iface__words__array] | None = ... # type:ignore[assignment,unused-ignore]
    vtt: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Large_V3_Turbo_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    audio: str = ... # type:ignore[assignment,unused-ignore]
    task: str | None = ... # type:ignore[assignment,unused-ignore]
    language: str | None = ... # type:ignore[assignment,unused-ignore]
    vad_filter: bool | None = ... # type:ignore[assignment,unused-ignore]
    initial_prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    prefix: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    transcription_info: Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__transcription_info | None = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    word_count: int | float | None = ... # type:ignore[assignment,unused-ignore]
    segments: JsArray[Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__segments__array] | None = ... # type:ignore[assignment,unused-ignore]
    vtt: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    steps: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Black_Forest_Labs_Flux_1_Schnell_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    image: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface__response_format | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    response: str | Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface__response__Union1 | None = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface__usage | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Reranker_Base_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    contexts: JsArray[Ai_Cf_Baai_Bge_Reranker_Base_Input_iface__contexts__array] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Reranker_Base_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    response: JsArray[Ai_Cf_Baai_Bge_Reranker_Base_Output_iface__response__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    audio: Ai_Cf_Deepgram_Nova_3_Input_iface__audio = ... # type:ignore[assignment,unused-ignore]
    custom_topic_mode: Literal["extended", "strict"] | None = ... # type:ignore[assignment,unused-ignore]
    custom_topic: str | None = ... # type:ignore[assignment,unused-ignore]
    custom_intent_mode: Literal["extended", "strict"] | None = ... # type:ignore[assignment,unused-ignore]
    custom_intent: str | None = ... # type:ignore[assignment,unused-ignore]
    detect_entities: bool | None = ... # type:ignore[assignment,unused-ignore]
    detect_language: bool | None = ... # type:ignore[assignment,unused-ignore]
    diarize: bool | None = ... # type:ignore[assignment,unused-ignore]
    dictation: bool | None = ... # type:ignore[assignment,unused-ignore]
    encoding: Literal["linear16", "flac", "mulaw", "amr-nb", "amr-wb", "opus", "speex", "g729"] | None = ... # type:ignore[assignment,unused-ignore]
    extra: str | None = ... # type:ignore[assignment,unused-ignore]
    filler_words: bool | None = ... # type:ignore[assignment,unused-ignore]
    keyterm: str | None = ... # type:ignore[assignment,unused-ignore]
    keywords: str | None = ... # type:ignore[assignment,unused-ignore]
    language: str | None = ... # type:ignore[assignment,unused-ignore]
    measurements: bool | None = ... # type:ignore[assignment,unused-ignore]
    mip_opt_out: bool | None = ... # type:ignore[assignment,unused-ignore]
    mode: Literal["general", "medical", "finance"] | None = ... # type:ignore[assignment,unused-ignore]
    multichannel: bool | None = ... # type:ignore[assignment,unused-ignore]
    numerals: bool | None = ... # type:ignore[assignment,unused-ignore]
    paragraphs: bool | None = ... # type:ignore[assignment,unused-ignore]
    profanity_filter: bool | None = ... # type:ignore[assignment,unused-ignore]
    punctuate: bool | None = ... # type:ignore[assignment,unused-ignore]
    redact: str | None = ... # type:ignore[assignment,unused-ignore]
    replace: str | None = ... # type:ignore[assignment,unused-ignore]
    search: str | None = ... # type:ignore[assignment,unused-ignore]
    sentiment: bool | None = ... # type:ignore[assignment,unused-ignore]
    smart_format: bool | None = ... # type:ignore[assignment,unused-ignore]
    topics: bool | None = ... # type:ignore[assignment,unused-ignore]
    utterances: bool | None = ... # type:ignore[assignment,unused-ignore]
    utt_split: int | float | None = ... # type:ignore[assignment,unused-ignore]
    channels: int | float | None = ... # type:ignore[assignment,unused-ignore]
    interim_results: bool | None = ... # type:ignore[assignment,unused-ignore]
    endpointing: str | None = ... # type:ignore[assignment,unused-ignore]
    vad_events: bool | None = ... # type:ignore[assignment,unused-ignore]
    utterance_end_ms: bool | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    results: Ai_Cf_Deepgram_Nova_3_Output_iface__results | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_Embedding_0_6B_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    queries: str | JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    instruction: str | None = ... # type:ignore[assignment,unused-ignore]
    documents: str | JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    text: str | JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_Embedding_0_6B_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    data: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    is_complete: bool | None = ... # type:ignore[assignment,unused-ignore]
    probability: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Leonardo_Phoenix_1_0_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guidance: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    height: int | float | None = ... # type:ignore[assignment,unused-ignore]
    width: int | float | None = ... # type:ignore[assignment,unused-ignore]
    num_steps: int | float | None = ... # type:ignore[assignment,unused-ignore]
    negative_prompt: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Leonardo_Lucid_Origin_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guidance: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    height: int | float | None = ... # type:ignore[assignment,unused-ignore]
    width: int | float | None = ... # type:ignore[assignment,unused-ignore]
    num_steps: int | float | None = ... # type:ignore[assignment,unused-ignore]
    steps: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Leonardo_Lucid_Origin_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    image: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Aura_1_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    speaker: Literal["angus", "asteria", "arcas", "orion", "orpheus", "athena", "luna", "zeus", "perseus", "helios", "hera", "stella"] | None = ... # type:ignore[assignment,unused-ignore]
    encoding: Literal["linear16", "flac", "mulaw", "alaw", "mp3", "opus", "aac"] | None = ... # type:ignore[assignment,unused-ignore]
    container: Literal["none", "wav", "ogg"] | None = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    sample_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]
    bit_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    target_language: Literal["asm_Beng", "awa_Deva", "ben_Beng", "bho_Deva", "brx_Deva", "doi_Deva", "eng_Latn", "gom_Deva", "gon_Deva", "guj_Gujr", "hin_Deva", "hne_Deva", "kan_Knda", "kas_Arab", "kas_Deva", "kha_Latn", "lus_Latn", "mag_Deva", "mai_Deva", "mal_Mlym", "mar_Deva", "mni_Beng", "mni_Mtei", "npi_Deva", "ory_Orya", "pan_Guru", "san_Deva", "sat_Olck", "snd_Arab", "snd_Deva", "tam_Taml", "tel_Telu", "urd_Arab", "unr_Deva"] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Ai4Bharat_Indictrans2_En_Indic_1B_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    translations: JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pfnet_Plamo_Embedding_1B_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pfnet_Plamo_Embedding_1B_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    data: JsArray[JsArray[int | float]] = ... # type:ignore[assignment,unused-ignore]
    shape: tuple[int | float, int | float] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Flux_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    encoding: Literal["linear16"] = ... # type:ignore[assignment,unused-ignore]
    sample_rate: str = ... # type:ignore[assignment,unused-ignore]
    eager_eot_threshold: str | None = ... # type:ignore[assignment,unused-ignore]
    eot_threshold: str | None = ... # type:ignore[assignment,unused-ignore]
    eot_timeout_ms: str | None = ... # type:ignore[assignment,unused-ignore]
    keyterm: str | None = ... # type:ignore[assignment,unused-ignore]
    mip_opt_out: Literal["true", "false"] | None = ... # type:ignore[assignment,unused-ignore]
    tag: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Flux_Output_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]
    sequence_id: int | float | None = ... # type:ignore[assignment,unused-ignore]
    event: Literal["Update", "StartOfTurn", "EagerEndOfTurn", "TurnResumed", "EndOfTurn"] | None = ... # type:ignore[assignment,unused-ignore]
    turn_index: int | float | None = ... # type:ignore[assignment,unused-ignore]
    audio_window_start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    audio_window_end: int | float | None = ... # type:ignore[assignment,unused-ignore]
    transcript: str | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[Ai_Cf_Deepgram_Flux_Output_iface__words__array] | None = ... # type:ignore[assignment,unused-ignore]
    end_of_turn_confidence: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Aura_2_En_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    speaker: Literal["amalthea", "andromeda", "apollo", "arcas", "aries", "asteria", "athena", "atlas", "aurora", "callista", "cora", "cordelia", "delia", "draco", "electra", "harmonia", "helena", "hera", "hermes", "hyperion", "iris", "janus", "juno", "jupiter", "luna", "mars", "minerva", "neptune", "odysseus", "ophelia", "orion", "orpheus", "pandora", "phoebe", "pluto", "saturn", "thalia", "theia", "vesta", "zeus"] | None = ... # type:ignore[assignment,unused-ignore]
    encoding: Literal["linear16", "flac", "mulaw", "alaw", "mp3", "opus", "aac"] | None = ... # type:ignore[assignment,unused-ignore]
    container: Literal["none", "wav", "ogg"] | None = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    sample_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]
    bit_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Aura_2_Es_Input_iface(Protocol): # type:ignore[misc, unused-ignore]
    speaker: Literal["sirio", "nestor", "carina", "celeste", "alvaro", "diana", "aquila", "selena", "estrella", "javier"] | None = ... # type:ignore[assignment,unused-ignore]
    encoding: Literal["linear16", "flac", "mulaw", "alaw", "mp3", "opus", "aac"] | None = ... # type:ignore[assignment,unused-ignore]
    container: Literal["none", "wav", "ogg"] | None = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    sample_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]
    bit_rate: int | float | None = ... # type:ignore[assignment,unused-ignore]

class AiModels_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class D1ExecResult_iface(Protocol): # type:ignore[misc, unused-ignore]
    count: int | float = ... # type:ignore[assignment,unused-ignore]
    duration: int | float = ... # type:ignore[assignment,unused-ignore]

class ForwardableEmailMessage_iface(EmailMessage_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def raw(self, /) -> ReadableStream[Uint8Array[ArrayBufferLike]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def headers(self, /) -> Headers: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def rawSize(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setReject(self, reason: str, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forward(self, rcptTo: str, headers: Headers | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reply(self, message: EmailMessage_iface, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reply(self, /, *, from_: str, to: str) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class VectorizeIndexDetails_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def id(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str | None = ... # type:ignore[assignment,unused-ignore]
    config: VectorizeIndexConfig = ... # type:ignore[assignment,unused-ignore]
    vectorsCount: int | float = ... # type:ignore[assignment,unused-ignore]

class VectorizeQueryOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    topK: int | float | None = ... # type:ignore[assignment,unused-ignore]
    namespace: str | None = ... # type:ignore[assignment,unused-ignore]
    returnValues: bool | None = ... # type:ignore[assignment,unused-ignore]
    returnMetadata: bool | VectorizeMetadataRetrievalLevel | None = ... # type:ignore[assignment,unused-ignore]
    filter: VectorizeVectorMetadataFilter | None = ... # type:ignore[assignment,unused-ignore]

class VectorizeMatches_iface(Protocol): # type:ignore[misc, unused-ignore]
    matches: JsArray[VectorizeMatch] = ... # type:ignore[assignment,unused-ignore]
    count: int | float = ... # type:ignore[assignment,unused-ignore]

class VectorizeVector_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    values: VectorFloatArray | JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]
    namespace: str | None = ... # type:ignore[assignment,unused-ignore]
    metadata: Record[str, VectorizeVectorMetadata] | None = ... # type:ignore[assignment,unused-ignore]

class VectorizeVectorMutation_iface(Protocol): # type:ignore[misc, unused-ignore]
    ids: JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    count: int | float = ... # type:ignore[assignment,unused-ignore]

class VectorizeIndexInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    vectorCount: int | float = ... # type:ignore[assignment,unused-ignore]
    dimensions: int | float = ... # type:ignore[assignment,unused-ignore]
    processedUpToDatetime: int | float = ... # type:ignore[assignment,unused-ignore]
    processedUpToMutation: int | float = ... # type:ignore[assignment,unused-ignore]

class VectorizeAsyncMutation_iface(Protocol): # type:ignore[misc, unused-ignore]
    mutationId: str = ... # type:ignore[assignment,unused-ignore]

class WorkflowInstanceCreateOptions_iface[PARAMS=Any](Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    params: PARAMS | None = ... # type:ignore[assignment,unused-ignore]
    retention: WorkflowInstanceCreateOptions_iface__retention | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectGetOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    allowConcurrency: bool | None = ... # type:ignore[assignment,unused-ignore]
    noCache: bool | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectPutOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    allowConcurrency: bool | None = ... # type:ignore[assignment,unused-ignore]
    allowUnconfirmed: bool | None = ... # type:ignore[assignment,unused-ignore]
    noCache: bool | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectListOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    start: str | None = ... # type:ignore[assignment,unused-ignore]
    startAfter: str | None = ... # type:ignore[assignment,unused-ignore]
    end: str | None = ... # type:ignore[assignment,unused-ignore]
    prefix: str | None = ... # type:ignore[assignment,unused-ignore]
    reverse: bool | None = ... # type:ignore[assignment,unused-ignore]
    limit: int | float | None = ... # type:ignore[assignment,unused-ignore]
    allowConcurrency: bool | None = ... # type:ignore[assignment,unused-ignore]
    noCache: bool | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectTransaction_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def get[T=Any](self, key: str, options: DurableObjectGetOptions_iface | None = None, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, key: str, /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, keys: PyMutableSequence[str], options: DurableObjectGetOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def get[T=Any](self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, options: DurableObjectListOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, /, *, start: str | None = None, startAfter: str | None = None, end: str | None = None, prefix: str | None = None, reverse: bool | None = None, limit: int | float | None = None, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, key: str, value: T, options: DurableObjectPutOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, key: str, value: T, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, entries: Record[str, T], options: DurableObjectPutOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def put[T](self, entries: Record[str, T], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, key: str, options: DurableObjectPutOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, key: str, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, keys: PyMutableSequence[str], options: DurableObjectPutOptions_iface | None = None, /) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def delete(self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def rollback(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getAlarm(self, options: DurableObjectGetAlarmOptions_iface | None = None, /) -> Future[int | float | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def getAlarm(self, /, *, allowConcurrency: bool | None = None) -> Future[int | float | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setAlarm(self, scheduledTime: int | float | Date, options: DurableObjectSetAlarmOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setAlarm(self, scheduledTime: int | float | Date, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAlarm(self, options: DurableObjectSetAlarmOptions_iface | None = None, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def deleteAlarm(self, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, key: str, options: DurableObjectGetOptions_iface | None = None, /) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, key: str, /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[T | None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, keys: PyMutableSequence[str], options: DurableObjectGetOptions_iface | None = None, /) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __getitem__[T=Any](self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, noCache: bool | None = None) -> Future[Map[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, key: str, options: DurableObjectPutOptions_iface | None = None, /) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, key: str, /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[bool]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, keys: PyMutableSequence[str], options: DurableObjectPutOptions_iface | None = None, /) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __delitem__(self, keys: PyMutableSequence[str], /, *, allowConcurrency: bool | None = None, allowUnconfirmed: bool | None = None, noCache: bool | None = None) -> Future[int | float]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectGetAlarmOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    allowConcurrency: bool | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectSetAlarmOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    allowConcurrency: bool | None = ... # type:ignore[assignment,unused-ignore]
    allowUnconfirmed: bool | None = ... # type:ignore[assignment,unused-ignore]

class SqlStorage_iface(Protocol): # type:ignore[misc, unused-ignore]
    Cursor: Any = ... # type:ignore[assignment,unused-ignore]
    Statement: Any = ... # type:ignore[assignment,unused-ignore]
    def exec[T](self, query: str, /, *bindings: Any) -> SqlStorageCursor[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SyncKvStorage_iface(Protocol): # type:ignore[misc, unused-ignore]
    def get[T=Any](self, key: str, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, options: SyncKvListOptions_iface | None = None, /) -> JsIterable[tuple[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def list[T=Any](self, /, *, start: str | None = None, startAfter: str | None = None, end: str | None = None, prefix: str | None = None, reverse: bool | None = None, limit: int | float | None = None) -> JsIterable[tuple[str, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def put[T](self, key: str, value: T, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def delete(self, key: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __getitem__[T=Any](self, key: str, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __delitem__(self, key: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ContainerStartupOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    entrypoint: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    enableInternet: bool = ... # type:ignore[assignment,unused-ignore]
    env: Record[str, str] | None = ... # type:ignore[assignment,unused-ignore]
    hardTimeout: (int | float | int) | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImage_iface(BasicImageTransformations_iface, Protocol): # type:ignore[misc, unused-ignore]
    dpr: int | float | None = ... # type:ignore[assignment,unused-ignore]
    trim: RequestInitCfPropertiesImage_iface__trim__Union0 | Literal["border"] | None = ... # type:ignore[assignment,unused-ignore]
    quality: int | float | Literal["low", "medium-low", "medium-high", "high"] | None = ... # type:ignore[assignment,unused-ignore]
    format: Literal["avif", "webp", "json", "jpeg", "png", "baseline-jpeg", "png-force", "svg"] | None = ... # type:ignore[assignment,unused-ignore]
    anim: bool | None = ... # type:ignore[assignment,unused-ignore]
    metadata: Literal["keep", "copyright", "none"] | None = ... # type:ignore[assignment,unused-ignore]
    sharpen: int | float | None = ... # type:ignore[assignment,unused-ignore]
    blur: int | float | None = ... # type:ignore[assignment,unused-ignore]
    draw: JsArray[RequestInitCfPropertiesImageDraw_iface] | None = ... # type:ignore[assignment,unused-ignore]
    border: RequestInitCfPropertiesImage_iface__border__Union0 | RequestInitCfPropertiesImage_iface__border__Union1 | None = ... # type:ignore[assignment,unused-ignore]
    brightness: int | float | None = ... # type:ignore[assignment,unused-ignore]
    contrast: int | float | None = ... # type:ignore[assignment,unused-ignore]
    gamma: int | float | None = ... # type:ignore[assignment,unused-ignore]
    saturation: int | float | None = ... # type:ignore[assignment,unused-ignore]
    flip: Literal['h', 'v', 'hv'] | None = ... # type:ignore[assignment,unused-ignore]
    compression: Literal["fast"] | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImageMinify_iface(Protocol): # type:ignore[misc, unused-ignore]
    javascript: bool | None = ... # type:ignore[assignment,unused-ignore]
    css: bool | None = ... # type:ignore[assignment,unused-ignore]
    html: bool | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesR2_iface(Protocol): # type:ignore[misc, unused-ignore]
    bucketColoId: int | float | None = ... # type:ignore[assignment,unused-ignore]

class SocketAddress_iface(Protocol): # type:ignore[misc, unused-ignore]
    hostname: str = ... # type:ignore[assignment,unused-ignore]
    port: int | float = ... # type:ignore[assignment,unused-ignore]

class SocketOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    secureTransport: str | None = ... # type:ignore[assignment,unused-ignore]
    allowHalfOpen: bool = ... # type:ignore[assignment,unused-ignore]
    highWaterMark: (int | float | int) | None = ... # type:ignore[assignment,unused-ignore]

class Socket_iface(Protocol): # type:ignore[misc, unused-ignore]
    def close(self, /) -> Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def startTls(self, options: TlsOptions_iface | None = None, /) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def startTls(self, /, *, expectedServerHostname: str | None = None) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadableStreamGetReaderOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    mode: Literal["byob"] = ... # type:ignore[assignment,unused-ignore]

class ReadableWritablePair_iface[R=Any, W=Any](Protocol): # type:ignore[misc, unused-ignore]
    writable: WritableStream[W] = ... # type:ignore[assignment,unused-ignore]
    readable: ReadableStream[R] = ... # type:ignore[assignment,unused-ignore]

class StreamPipeOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    preventClose: bool | None = ... # type:ignore[assignment,unused-ignore]
    preventAbort: bool | None = ... # type:ignore[assignment,unused-ignore]
    preventCancel: bool | None = ... # type:ignore[assignment,unused-ignore]
    signal: AbortSignal | None = ... # type:ignore[assignment,unused-ignore]

class ReadableStreamValuesOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    preventCancel: bool | None = ... # type:ignore[assignment,unused-ignore]

class StringIterator_iface[T](IteratorObject_iface[T, BuiltinIteratorReturn, Any]): # type:ignore[misc, unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RegExpMatchArray_iface(Array_iface[str]): # type:ignore[misc, unused-ignore]
    index: int | None = ... # type:ignore[assignment,unused-ignore]
    input: str | None = ... # type:ignore[assignment,unused-ignore]
    groups: RegExpMatchArray_iface__groups | None = ... # type:ignore[assignment,unused-ignore]
    indices: RegExpIndicesArray_iface | None = ... # type:ignore[assignment,unused-ignore]

class RegExpExecArray_iface(Array_iface[str]): # type:ignore[misc, unused-ignore]
    index: int = ... # type:ignore[assignment,unused-ignore]
    input: str = ... # type:ignore[assignment,unused-ignore]
    groups: RegExpExecArray_iface__groups | None = ... # type:ignore[assignment,unused-ignore]
    indices: RegExpIndicesArray_iface | None = ... # type:ignore[assignment,unused-ignore]

class RegExpStringIterator_iface[T](IteratorObject_iface[T, BuiltinIteratorReturn, Any]): # type:ignore[misc, unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ArrayIterator_iface[T](IteratorObject_iface[T, BuiltinIteratorReturn, Any]): # type:ignore[misc, unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SetIterator_iface[T](IteratorObject_iface[T, BuiltinIteratorReturn, Any]): # type:ignore[misc, unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadonlySetLike_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def size(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> JsGenerator[T, Any, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def has(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, value: T, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class BigIntToLocaleStringOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    localeMatcher: str | None = ... # type:ignore[assignment,unused-ignore]
    style: str | None = ... # type:ignore[assignment,unused-ignore]
    numberingSystem: str | None = ... # type:ignore[assignment,unused-ignore]
    unit: str | None = ... # type:ignore[assignment,unused-ignore]
    unitDisplay: str | None = ... # type:ignore[assignment,unused-ignore]
    currency: str | None = ... # type:ignore[assignment,unused-ignore]
    currencyDisplay: str | None = ... # type:ignore[assignment,unused-ignore]
    useGrouping: bool | None = ... # type:ignore[assignment,unused-ignore]
    minimumIntegerDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = ... # type:ignore[assignment,unused-ignore]
    minimumFractionDigits: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | None = ... # type:ignore[assignment,unused-ignore]
    maximumFractionDigits: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] | None = ... # type:ignore[assignment,unused-ignore]
    minimumSignificantDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = ... # type:ignore[assignment,unused-ignore]
    maximumSignificantDigits: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21] | None = ... # type:ignore[assignment,unused-ignore]
    notation: str | None = ... # type:ignore[assignment,unused-ignore]
    compactDisplay: str | None = ... # type:ignore[assignment,unused-ignore]

class EventListenerObject_iface[EventType=Event](Protocol): # type:ignore[misc, unused-ignore]
    def handleEvent(self, event: EventType, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class QueueEvent_iface[Body=Any](ExtendableEvent_iface, Protocol): # type:ignore[misc, unused-ignore]
    @property
    def messages(self, /) -> JsArray[Message_iface[Body]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def queue(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def retryAll(self, options: QueueRetryOptions_iface | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def retryAll(self, /, *, delaySeconds: int | float | None = None) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def ackAll(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RsaOtherPrimesInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    r: str | None = ... # type:ignore[assignment,unused-ignore]
    d: str | None = ... # type:ignore[assignment,unused-ignore]
    t: str | None = ... # type:ignore[assignment,unused-ignore]

class Element_iface(Protocol): # type:ignore[misc, unused-ignore]
    tagName: str = ... # type:ignore[assignment,unused-ignore]
    @property
    def attributes(self, /) -> JsIterator[JsArray[str]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def removed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def namespaceURI(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getAttribute(self, name: str, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def hasAttribute(self, name: str, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def setAttribute(self, name: str, value: str, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def removeAttribute(self, name: str, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def prepend(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def prepend(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def append(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def append(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def remove(self, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def removeAndKeepContent(self, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setInnerContent(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def setInnerContent(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Element_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def onEndTag(self, handler: Element_iface__onEndTag__Sig0__handler, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Comment_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    @property
    def removed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str, options: ContentOptions_iface | None = None, /) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str, /, *, html: bool | None = None) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str, options: ContentOptions_iface | None = None, /) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str, /, *, html: bool | None = None) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str, options: ContentOptions_iface | None = None, /) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str, /, *, html: bool | None = None) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def remove(self, /) -> Comment_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Text_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def text(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def lastInTextNode(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def removed(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def replace(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def remove(self, /) -> Text_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Doctype_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def name(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def publicId(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def systemId(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DocumentEnd_iface(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def append(self, content: str, options: ContentOptions_iface | None = None, /) -> DocumentEnd_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def append(self, content: str, /, *, html: bool | None = None) -> DocumentEnd_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2UploadPartOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    ssecKey: (ArrayBuffer | str) | None = ... # type:ignore[assignment,unused-ignore]

class R2UploadedPart_iface(Protocol): # type:ignore[misc, unused-ignore]
    partNumber: int | float = ... # type:ignore[assignment,unused-ignore]
    etag: str = ... # type:ignore[assignment,unused-ignore]

class R2StringChecksums_iface(Protocol): # type:ignore[misc, unused-ignore]
    md5: str | None = ... # type:ignore[assignment,unused-ignore]
    sha1: str | None = ... # type:ignore[assignment,unused-ignore]
    sha256: str | None = ... # type:ignore[assignment,unused-ignore]
    sha384: str | None = ... # type:ignore[assignment,unused-ignore]
    sha512: str | None = ... # type:ignore[assignment,unused-ignore]

class TraceItemFetchEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def response(self, /) -> TraceItemFetchEventInfoResponse_iface | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def request(self, /) -> TraceItemFetchEventInfoRequest_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemJsRpcEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def rpcMethod(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemScheduledEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def scheduledTime(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def cron(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemAlarmEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def scheduledTime(self, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemQueueEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def queue(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def batchSize(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemEmailEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def mailFrom(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def rcptTo(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def rawSize(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemTailEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def consumedEvents(self, /) -> JsArray[TraceItemTailEventInfoTailItem_iface]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemCustomEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class TraceItemHibernatableWebSocketEventInfo_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def getWebSocketEvent(self, /) -> TraceItemHibernatableWebSocketEventInfoMessage_iface | TraceItemHibernatableWebSocketEventInfoClose_iface | TraceItemHibernatableWebSocketEventInfoError_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceLog_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def timestamp(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def level(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def message(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceException_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def timestamp(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def message(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def name(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def stack(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceDiagnosticChannelEvent_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def timestamp(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def channel(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def message(self, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ScriptVersion_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    tag: str | None = ... # type:ignore[assignment,unused-ignore]
    message: str | None = ... # type:ignore[assignment,unused-ignore]

class URLPatternComponentResult_iface(Protocol): # type:ignore[misc, unused-ignore]
    input: str = ... # type:ignore[assignment,unused-ignore]
    groups: Record[str, str] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Base_En_V1_5_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_M2M100_1_2B_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Small_En_V1_5_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Large_En_V1_5_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_iface(Protocol): # type:ignore[misc, unused-ignore]
    query: str | None = ... # type:ignore[assignment,unused-ignore]
    contexts: JsArray[Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_iface__contexts__array] = ... # type:ignore[assignment,unused-ignore]
    truncate_inputs: bool | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_Embedding_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    truncate_inputs: bool | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    query: str | None = ... # type:ignore[assignment,unused-ignore]
    contexts: JsArray[Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_1_iface__contexts__array] = ... # type:ignore[assignment,unused-ignore]
    truncate_inputs: bool | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_Embedding_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    truncate_inputs: bool | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Ouput_Query_iface(Protocol): # type:ignore[misc, unused-ignore]
    response: JsArray[Ai_Cf_Baai_Bge_M3_Ouput_Query_iface__response__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Output_EmbeddingFor_Contexts_iface(Protocol): # type:ignore[misc, unused-ignore]
    response: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Ouput_Embedding_iface(Protocol): # type:ignore[misc, unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    image: JsArray[int | float] | (Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Prompt_iface__image__Union1) | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    image: JsArray[int | float] | (Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__image__Union1) | None = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0 | Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0 | Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_1_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Async_Batch_iface(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Async_Batch_iface__requests__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0 | Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_JSON_Mode_1_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Qwen_Qwq_32B_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0 | Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0 | Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0 | Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0 | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Async_Batch_iface(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[(Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Prompt_Inner_iface | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface)] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0 | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_1_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Async_Batch_iface(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[(Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Prompt_1_iface | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface)] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    object: Literal["chat.completion"] | None = ... # type:ignore[assignment,unused-ignore]
    created: int | float | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]
    choices: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array] | None = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__usage | None = ... # type:ignore[assignment,unused-ignore]
    prompt_logprobs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__prompt_logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    object: Literal["text_completion"] | None = ... # type:ignore[assignment,unused-ignore]
    created: int | float | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]
    choices: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array] | None = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__usage | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Prompt_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0 | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_1_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Async_Batch_iface(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[(Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Prompt_1_iface | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface)] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    object: Literal["chat.completion"] | None = ... # type:ignore[assignment,unused-ignore]
    created: int | float | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]
    choices: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array] | None = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__usage | None = ... # type:ignore[assignment,unused-ignore]
    prompt_logprobs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__prompt_logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    object: Literal["text_completion"] | None = ... # type:ignore[assignment,unused-ignore]
    created: int | float | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]
    choices: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array] | None = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__usage | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_AsyncResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    request_id: str | None = ... # type:ignore[assignment,unused-ignore]

class D1Response_iface(Protocol): # type:ignore[misc, unused-ignore]
    success: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    meta: D1Response_iface__meta = ... # type:ignore[assignment,unused-ignore]
    error: Never | None = ... # type:ignore[assignment,unused-ignore]

class EmailMessage_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def from_(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def to(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class SyncKvListOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    start: str | None = ... # type:ignore[assignment,unused-ignore]
    startAfter: str | None = ... # type:ignore[assignment,unused-ignore]
    end: str | None = ... # type:ignore[assignment,unused-ignore]
    prefix: str | None = ... # type:ignore[assignment,unused-ignore]
    reverse: bool | None = ... # type:ignore[assignment,unused-ignore]
    limit: int | float | None = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesBase_iface(Protocol): # type:ignore[misc, unused-ignore]
    asn: int | float | None = ... # type:ignore[assignment,unused-ignore]
    asOrganization: str | None = ... # type:ignore[assignment,unused-ignore]
    clientAcceptEncoding: str | None = ... # type:ignore[assignment,unused-ignore]
    clientTcpRtt: int | float | None = ... # type:ignore[assignment,unused-ignore]
    colo: str = ... # type:ignore[assignment,unused-ignore]
    edgeRequestKeepAliveStatus: IncomingRequestCfPropertiesEdgeRequestKeepAliveStatus = ... # type:ignore[assignment,unused-ignore]
    httpProtocol: str = ... # type:ignore[assignment,unused-ignore]
    requestPriority: str = ... # type:ignore[assignment,unused-ignore]
    tlsVersion: str = ... # type:ignore[assignment,unused-ignore]
    tlsCipher: str = ... # type:ignore[assignment,unused-ignore]
    tlsExportedAuthenticator: IncomingRequestCfPropertiesExportedAuthenticatorMetadata_iface | None = ... # type:ignore[assignment,unused-ignore]
    def __getattr__(self, key: str, /) -> Any: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class IncomingRequestCfPropertiesBotManagementEnterprise_iface(IncomingRequestCfPropertiesBotManagement_iface, Protocol): # type:ignore[misc, unused-ignore]
    botManagement: IncomingRequestCfPropertiesBotManagementEnterprise_iface__botManagement = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesCloudflareForSaaSEnterprise_iface[HostMetadata](Protocol): # type:ignore[misc, unused-ignore]
    hostMetadata: HostMetadata | None = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesGeographicInformation_iface(Protocol): # type:ignore[misc, unused-ignore]
    country: Iso3166Alpha2Code | Literal["T1"] | None = ... # type:ignore[assignment,unused-ignore]
    isEUCountry: Literal["1"] | None = ... # type:ignore[assignment,unused-ignore]
    continent: ContinentCode | None = ... # type:ignore[assignment,unused-ignore]
    city: str | None = ... # type:ignore[assignment,unused-ignore]
    postalCode: str | None = ... # type:ignore[assignment,unused-ignore]
    latitude: str | None = ... # type:ignore[assignment,unused-ignore]
    longitude: str | None = ... # type:ignore[assignment,unused-ignore]
    timezone: str | None = ... # type:ignore[assignment,unused-ignore]
    region: str | None = ... # type:ignore[assignment,unused-ignore]
    regionCode: str | None = ... # type:ignore[assignment,unused-ignore]
    metroCode: str | None = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesCloudflareAccessOrApiShield_iface(Protocol): # type:ignore[misc, unused-ignore]
    tlsClientAuth: IncomingRequestCfPropertiesTLSClientAuth_iface | IncomingRequestCfPropertiesTLSClientAuthPlaceholder_iface = ... # type:ignore[assignment,unused-ignore]

class BasicImageTransformations_iface(Protocol): # type:ignore[misc, unused-ignore]
    width: int | float | None = ... # type:ignore[assignment,unused-ignore]
    height: int | float | None = ... # type:ignore[assignment,unused-ignore]
    fit: Literal["scale-down", "contain", "cover", "crop", "pad", "squeeze"] | None = ... # type:ignore[assignment,unused-ignore]
    segment: Literal["foreground"] | None = ... # type:ignore[assignment,unused-ignore]
    gravity: BasicImageTransformationsGravityCoordinates_iface | Literal['face', 'left', 'right', 'top', 'bottom', 'center', 'auto', 'entropy'] | None = ... # type:ignore[assignment,unused-ignore]
    background: str | None = ... # type:ignore[assignment,unused-ignore]
    rotate: Literal[0, 90, 180, 270, 360] | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImageDraw_iface(BasicImageTransformations_iface, Protocol): # type:ignore[misc, unused-ignore]
    url: str = ... # type:ignore[assignment,unused-ignore]
    opacity: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repeat: Literal[True, "x", "y"] | None = ... # type:ignore[assignment,unused-ignore]
    top: int | float | None = ... # type:ignore[assignment,unused-ignore]
    left: int | float | None = ... # type:ignore[assignment,unused-ignore]
    bottom: int | float | None = ... # type:ignore[assignment,unused-ignore]
    right: int | float | None = ... # type:ignore[assignment,unused-ignore]

class TlsOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    expectedServerHostname: str | None = ... # type:ignore[assignment,unused-ignore]

class IteratorObject_iface[T, TReturn=Any, TNext=Any](Disposable_iface, JsGenerator[T, TNext, TReturn]): # type:ignore[misc, unused-ignore]
    def map[U](self, callbackfn: Callable[[T, int | float], U], /) -> IteratorObject_iface[U, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter[S](self, predicate: Callable[[T, int | float], bool], /) -> IteratorObject_iface[S, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter(self, predicate: Callable[[T, int | float], Any], /) -> IteratorObject_iface[T, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def take(self, limit: int | float, /) -> IteratorObject_iface[T, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def drop(self, count: int | float, /) -> IteratorObject_iface[T, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def flatMap[U](self, callback: Callable[[T, int | float], PyGenerator[U, None, Any] | PyIterable[U]], /) -> IteratorObject_iface[U, None, Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int | float], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int | float], T], initialValue: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, T, int | float], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toArray(self, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[T, int | float], None], /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[T, int | float], Any], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def every(self, predicate: Callable[[T, int | float], Any], /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find[S](self, predicate: Callable[[T, int | float], bool], /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find(self, predicate: Callable[[T, int | float], Any], /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Array_iface[T](JsArray[T]): # type:ignore[misc, unused-ignore]
    length: int = ... # type:ignore[assignment,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def pop(self, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def push(self, /, *items: T) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def concat(self, /, *items: ConcatArray_iface[T]) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def concat(self, /, *items: (T | ConcatArray_iface[T])) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def reverse(self, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def shift(self, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def sort(self, compareFn: Callable[[T, T], int] | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def splice(self, start: int, deleteCount: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def splice(self, start: int, deleteCount: int, /, *items: T) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def unshift(self, /, *items: T) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: T, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: T, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def every[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def every(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[T, int, JsArray[T]], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map[U](self, callbackfn: Callable[[T, int, JsArray[T]], U], thisArg: Any | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> JsArray[S]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], initialValue: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, T, int, JsArray[T]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], initialValue: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, T, int, JsArray[T]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def fill(self, value: T, start: int | None = None, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def copyWithin(self, target: int, start: int, end: int | None = None, /) -> Self: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: T, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def flatMap[U, This=None](self, callback: Callable[[This, T, int, JsArray[T]], U | ReadonlyArray_iface[U]], thisArg: This | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def flat[A, D=Literal[1]](self, this: A, depth: D | None = None, /) -> JsArray[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[T, T], int] | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toSpliced(self, start: int, deleteCount: int, /, *items: T) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toSpliced(self, start: int, deleteCount: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: T, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: T, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RegExpIndicesArray_iface(Array_iface[tuple[int | float, int | float]]): # type:ignore[misc, unused-ignore]
    groups: RegExpIndicesArray_iface__groups | None = ... # type:ignore[assignment,unused-ignore]

class QueueRetryOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    delaySeconds: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Message_iface[Body=Any](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def id(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def timestamp(self, /) -> Date: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def body(self, /) -> Body: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def attempts(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def retry(self, options: QueueRetryOptions_iface | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def retry(self, /, *, delaySeconds: int | float | None = None) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def ack(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ContentOptions_iface(Protocol): # type:ignore[misc, unused-ignore]
    html: bool | None = ... # type:ignore[assignment,unused-ignore]

class EndTag_iface(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> EndTag_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def before(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> EndTag_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, options: ContentOptions_iface | None = None, /) -> EndTag_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def after(self, content: str | ReadableStream[Any] | Response, /, *, html: bool | None = None) -> EndTag_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def remove(self, /) -> EndTag_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemFetchEventInfoResponse_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def status(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemFetchEventInfoRequest_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def cf(self, /) -> Any | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def headers(self, /) -> Record[str, str]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def method(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def url(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def getUnredacted(self, /) -> TraceItemFetchEventInfoRequest_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemTailEventInfoTailItem_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def scriptName(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemHibernatableWebSocketEventInfoMessage_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def webSocketEventType(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemHibernatableWebSocketEventInfoClose_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def webSocketEventType(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def code(self, /) -> int | float: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def wasClean(self, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class TraceItemHibernatableWebSocketEventInfoError_iface(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def webSocketEventType(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_2_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_JSON_Mode_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_JSON_Mode_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_JSON_Mode_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Prompt_Inner_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0 | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_JSON_Mode_iface | None = ... # type:ignore[assignment,unused-ignore]
    guided_json: Any | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Prompt_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_2_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0 | Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_3_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Prompt_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lora: str | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_2_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface(Protocol): # type:ignore[misc, unused-ignore]
    messages: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__messages__array] = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__functions__array] | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[(Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0 | Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1)] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_3_iface | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]

class D1Meta_iface(Protocol): # type:ignore[misc, unused-ignore]
    duration: int | float = ... # type:ignore[assignment,unused-ignore]
    size_after: int | float = ... # type:ignore[assignment,unused-ignore]
    rows_read: int | float = ... # type:ignore[assignment,unused-ignore]
    rows_written: int | float = ... # type:ignore[assignment,unused-ignore]
    last_row_id: int | float = ... # type:ignore[assignment,unused-ignore]
    changed_db: bool = ... # type:ignore[assignment,unused-ignore]
    changes: int | float = ... # type:ignore[assignment,unused-ignore]
    served_by_region: str | None = ... # type:ignore[assignment,unused-ignore]
    served_by_primary: bool | None = ... # type:ignore[assignment,unused-ignore]
    timings: D1Meta_iface__timings | None = ... # type:ignore[assignment,unused-ignore]
    total_attempts: int | float | None = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesExportedAuthenticatorMetadata_iface(Protocol): # type:ignore[misc, unused-ignore]
    clientHandshake: str = ... # type:ignore[assignment,unused-ignore]
    serverHandshake: str = ... # type:ignore[assignment,unused-ignore]
    clientFinished: str = ... # type:ignore[assignment,unused-ignore]
    serverFinished: str = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesBotManagement_iface(Protocol): # type:ignore[misc, unused-ignore]
    botManagement: IncomingRequestCfPropertiesBotManagementBase_iface = ... # type:ignore[assignment,unused-ignore]
    clientTrustScore: int | float = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesBotManagementBase_iface(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float = ... # type:ignore[assignment,unused-ignore]
    verifiedBot: bool = ... # type:ignore[assignment,unused-ignore]
    corporateProxy: bool = ... # type:ignore[assignment,unused-ignore]
    staticResource: bool = ... # type:ignore[assignment,unused-ignore]
    detectionIds: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesTLSClientAuth_iface(Protocol): # type:ignore[misc, unused-ignore]
    certPresented: Literal["1"] = ... # type:ignore[assignment,unused-ignore]
    certVerified: CertVerificationStatus = ... # type:ignore[assignment,unused-ignore]
    certRevoked: Literal["1", "0"] = ... # type:ignore[assignment,unused-ignore]
    certIssuerDN: str = ... # type:ignore[assignment,unused-ignore]
    certSubjectDN: str = ... # type:ignore[assignment,unused-ignore]
    certIssuerDNRFC2253: str = ... # type:ignore[assignment,unused-ignore]
    certSubjectDNRFC2253: str = ... # type:ignore[assignment,unused-ignore]
    certIssuerDNLegacy: str = ... # type:ignore[assignment,unused-ignore]
    certSubjectDNLegacy: str = ... # type:ignore[assignment,unused-ignore]
    certSerial: str = ... # type:ignore[assignment,unused-ignore]
    certIssuerSerial: str = ... # type:ignore[assignment,unused-ignore]
    certSKI: str = ... # type:ignore[assignment,unused-ignore]
    certIssuerSKI: str = ... # type:ignore[assignment,unused-ignore]
    certFingerprintSHA1: str = ... # type:ignore[assignment,unused-ignore]
    certFingerprintSHA256: str = ... # type:ignore[assignment,unused-ignore]
    certNotBefore: str = ... # type:ignore[assignment,unused-ignore]
    certNotAfter: str = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesTLSClientAuthPlaceholder_iface(Protocol): # type:ignore[misc, unused-ignore]
    certPresented: Literal["0"] = ... # type:ignore[assignment,unused-ignore]
    certVerified: Literal["NONE"] = ... # type:ignore[assignment,unused-ignore]
    certRevoked: Literal["0"] = ... # type:ignore[assignment,unused-ignore]
    certIssuerDN: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certSubjectDN: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certIssuerDNRFC2253: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certSubjectDNRFC2253: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certIssuerDNLegacy: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certSubjectDNLegacy: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certSerial: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certIssuerSerial: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certSKI: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certIssuerSKI: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certFingerprintSHA1: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certFingerprintSHA256: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certNotBefore: Literal[""] = ... # type:ignore[assignment,unused-ignore]
    certNotAfter: Literal[""] = ... # type:ignore[assignment,unused-ignore]

class BasicImageTransformationsGravityCoordinates_iface(Protocol): # type:ignore[misc, unused-ignore]
    x: int | float | None = ... # type:ignore[assignment,unused-ignore]
    y: int | float | None = ... # type:ignore[assignment,unused-ignore]
    mode: Literal['remainder', 'box-center'] | None = ... # type:ignore[assignment,unused-ignore]

class Disposable_iface(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ConcatArray_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ReadonlyArray_iface[T](Protocol): # type:ignore[misc, unused-ignore]
    @property
    def length(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toLocaleString(self, locales: str | PyMutableSequence[str], options: Any | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def concat(self, /, *items: ConcatArray_iface[T]) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def concat(self, /, *items: (T | ConcatArray_iface[T])) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def join(self, separator: str | None = None, /) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def slice(self, start: int | None = None, end: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def indexOf(self, searchElement: T, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def lastIndexOf(self, searchElement: T, fromIndex: int | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def every[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def every(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def some(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def forEach(self, callbackfn: Callable[[T, int, JsArray[T]], None], thisArg: Any | None = None, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def map[U](self, callbackfn: Callable[[T, int, JsArray[T]], U], thisArg: Any | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> JsArray[S]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def filter(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], initialValue: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduce[U](self, callbackfn: Callable[[U, T, int, JsArray[T]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight(self, callbackfn: Callable[[T, T, int, JsArray[T]], T], initialValue: T, /) -> T: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def reduceRight[U](self, callbackfn: Callable[[U, T, int, JsArray[T]], U], initialValue: U, /) -> U: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def find(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findIndex(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def entries(self, /) -> ArrayIterator_iface[tuple[int, T]]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def keys(self, /) -> ArrayIterator_iface[int]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def values(self, /) -> ArrayIterator_iface[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def includes(self, searchElement: T, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def flatMap[U, This=None](self, callback: Callable[[This, T, int, JsArray[T]], U | ReadonlyArray_iface[U]], thisArg: This | None = None, /) -> JsArray[U]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def flat[A, D=Literal[1]](self, this: A, depth: D | None = None, /) -> JsArray[Any]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def at(self, index: int, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast[S](self, predicate: Callable[[T, int, JsArray[T]], bool], thisArg: Any | None = None, /) -> S | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def findLast(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> T | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def findLastIndex(self, predicate: Callable[[T, int, JsArray[T]], Any], thisArg: Any | None = None, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toReversed(self, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def toSorted(self, compareFn: Callable[[T, T], int] | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toSpliced(self, start: int, deleteCount: int, /, *items: T) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def toSpliced(self, start: int, deleteCount: int | None = None, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def with_(self, index: int, value: T, /) -> JsArray[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __iter__(self, /) -> PyIterator[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    def __contains__(self, searchElement: T, fromIndex: int | None = None, /) -> bool: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_2_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_JSON_Mode_3_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_2_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_JSON_Mode_3_iface(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object", "json_schema"] | None = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class self__setTimeout__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class self__setTimeout__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class self__setInterval__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class self__setInterval__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Object__create__Sig1__properties(ThisType_iface[Any], PropertyDescriptorMap_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__defineProperty__Sig0__attributes(ThisType_iface[Any], PropertyDescriptor_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__defineProperties__Sig0__properties(ThisType_iface[Any], PropertyDescriptorMap_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__values__Sig0__o__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__entries__Sig0__o__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__getOwnPropertyDescriptors__Sig0__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__getOwnPropertyDescriptors__Sig0(Object__getOwnPropertyDescriptors__Sig0__Intersection1, Protocol): # type:ignore[misc, unused-ignore]
    pass

class Object__fromEntries__Sig0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class String__raw__Sig0__template(Protocol): # type:ignore[misc, unused-ignore]
    raw: JsArray[str] | ArrayLike_iface[str] = ... # type:ignore[assignment,unused-ignore]

class Proxy__revocable__Sig0[T](Protocol): # type:ignore[misc, unused-ignore]
    proxy: T = ... # type:ignore[assignment,unused-ignore]
    def revoke(self, /) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Atomics__waitAsync__Sig0__Union0(Protocol): # type:ignore[misc, unused-ignore]
    async_: Literal[False] = ... # type:ignore[assignment,unused-ignore]
    value: Literal["not-equal", "timed-out"] = ... # type:ignore[assignment,unused-ignore]

class Atomics__waitAsync__Sig0__Union1(Protocol): # type:ignore[misc, unused-ignore]
    async_: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    value: Future[Literal["ok", "timed-out"]] = ... # type:ignore[assignment,unused-ignore]

class Atomics__waitAsync__Sig1__Union0(Protocol): # type:ignore[misc, unused-ignore]
    async_: Literal[False] = ... # type:ignore[assignment,unused-ignore]
    value: Literal["not-equal", "timed-out"] = ... # type:ignore[assignment,unused-ignore]

class Atomics__waitAsync__Sig1__Union1(Protocol): # type:ignore[misc, unused-ignore]
    async_: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    value: Future[Literal["ok", "timed-out"]] = ... # type:ignore[assignment,unused-ignore]

class setTimeout__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class setTimeout__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class setInterval__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class setInterval__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2Bucket____getitem____Sig0__options__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    onlyIf: R2Conditional_iface | Headers = ... # type:ignore[assignment,unused-ignore]

class R2Bucket____getitem____Sig0__options(R2Bucket____getitem____Sig0__options__Intersection1, R2GetOptions_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class R2Bucket__get__Sig0__options__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    onlyIf: R2Conditional_iface | Headers = ... # type:ignore[assignment,unused-ignore]

class R2Bucket__get__Sig0__options(R2Bucket__get__Sig0__options__Intersection1, R2GetOptions_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class R2Bucket__put__Sig0__options__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    onlyIf: R2Conditional_iface | Headers = ... # type:ignore[assignment,unused-ignore]

class R2Bucket__put__Sig0__options(R2Bucket__put__Sig0__options__Intersection1, R2PutOptions_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class SqlStorageCursor__next__Sig0__Union0[T](Protocol): # type:ignore[misc, unused-ignore]
    done: Literal[False] | None = ... # type:ignore[assignment,unused-ignore]
    value: T = ... # type:ignore[assignment,unused-ignore]

class SqlStorageCursor__next__Sig0__Union1(Protocol): # type:ignore[misc, unused-ignore]
    done: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    value: Never | None = ... # type:ignore[assignment,unused-ignore]

class Workflow__create__Sig0(Protocol): # type:ignore[misc, unused-ignore]
    successRetention: WorkflowRetentionDuration | None = ... # type:ignore[assignment,unused-ignore]
    errorRetention: WorkflowRetentionDuration | None = ... # type:ignore[assignment,unused-ignore]

class DurableObjectStorage_iface__transaction__Sig0__closure[T](Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def __call__(self, txn: DurableObjectTransaction_iface, /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __call__(self, /) -> Future[T]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Fetcher__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, init: RequestInit_iface[CfProperties[Any]] | None = None, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: CfProperties[Any] | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def connect(self, address: SocketAddress_iface | str, options: SocketOptions_iface | None = None, /) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def connect(self, address: SocketAddress_iface | str, /, *, secureTransport: str | None = None, allowHalfOpen: bool, highWaterMark: (int | float | int) | None = None) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class Fetcher[T=None, Reserved=Never](Fetcher__Intersection1, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ServiceWorkerGlobalScope_iface__setTimeout__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ServiceWorkerGlobalScope_iface__setTimeout__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ServiceWorkerGlobalScope_iface__setInterval__Sig0__callback(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: Any) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class ServiceWorkerGlobalScope_iface__setInterval__Sig1__callback[*Args](Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, /, *args: *Args) -> None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class String_iface__replace__Sig1__replacer(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, substring: str, /, *args: Any) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class String_iface__replace__Sig2__searchValue(Protocol): # type:ignore[misc, unused-ignore]
    pass

class String_iface__replace__Sig3__searchValue(Protocol): # type:ignore[misc, unused-ignore]
    pass

class String_iface__replace__Sig3__replacer(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, substring: str, /, *args: Any) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class String_iface__split__Sig1__splitter(Protocol): # type:ignore[misc, unused-ignore]
    pass

class String_iface__replaceAll__Sig1__replacer(Protocol): # type:ignore[misc, unused-ignore]
    def __call__(self, substring: str, /, *args: Any) -> str: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class WorkerGlobalScopeEventMap(Protocol): # type:ignore[misc, unused-ignore]
    fetch: FetchEvent = ... # type:ignore[assignment,unused-ignore]
    scheduled: ScheduledEvent = ... # type:ignore[assignment,unused-ignore]
    queue: QueueEvent_iface[Any] = ... # type:ignore[assignment,unused-ignore]
    unhandledrejection: PromiseRejectionEvent = ... # type:ignore[assignment,unused-ignore]
    rejectionhandled: PromiseRejectionEvent = ... # type:ignore[assignment,unused-ignore]

class DurableObjectStub__Intersection0__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, init: RequestInit_iface[CfProperties[Any]] | None = None, /) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def fetch(self, input: RequestInfo[Any, CfProperties[Any]] | URL_, /, *, method: str | None = None, headers: HeadersInit | None = None, body: BodyInit | None = None, redirect: str | None = None, fetcher: (Fetcher[None, Never] | None) | None = None, cf: CfProperties[Any] | None = None, cache: Literal["no-store", "no-cache"] | None = None, integrity: str | None = None, signal: (AbortSignal | None) | None = None, encodeResponseBody: Literal["automatic", "manual"] | None = None) -> Future[Response]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def connect(self, address: SocketAddress_iface | str, options: SocketOptions_iface | None = None, /) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def connect(self, address: SocketAddress_iface | str, /, *, secureTransport: str | None = None, allowHalfOpen: bool, highWaterMark: (int | float | int) | None = None) -> Socket_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectStub__Intersection0(DurableObjectStub__Intersection0__Intersection1, Protocol): # type:ignore[misc, unused-ignore]
    pass

class DurableObjectStub__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    @property
    def id(self, /) -> DurableObjectId_iface: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @property
    def name(self, /) -> str | None: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class DurableObjectStub[T=None](DurableObjectStub__Intersection1, DurableObjectStub__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class R2Range__Union0(Protocol): # type:ignore[misc, unused-ignore]
    offset: int | float = ... # type:ignore[assignment,unused-ignore]
    length: int | float | None = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2Range__Union1(Protocol): # type:ignore[misc, unused-ignore]
    offset: int | float | None = ... # type:ignore[assignment,unused-ignore]
    length: int | float = ... # type:ignore[assignment,unused-ignore]
    def __len__(self, /) -> int: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class R2Range__Union2(Protocol): # type:ignore[misc, unused-ignore]
    suffix: int | float = ... # type:ignore[assignment,unused-ignore]

class R2Objects__Intersection0(Protocol): # type:ignore[misc, unused-ignore]
    objects: JsArray[R2Object] = ... # type:ignore[assignment,unused-ignore]
    delimitedPrefixes: JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class R2Objects__Intersection1__Union0(Protocol): # type:ignore[misc, unused-ignore]
    truncated: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    cursor: str = ... # type:ignore[assignment,unused-ignore]

class R2Objects__Intersection1__Union1(Protocol): # type:ignore[misc, unused-ignore]
    truncated: Literal[False] = ... # type:ignore[assignment,unused-ignore]

class R2Objects(R2Objects__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ReadableStreamReadResult__Union0[R](Protocol): # type:ignore[misc, unused-ignore]
    done: Literal[False] = ... # type:ignore[assignment,unused-ignore]
    value: R = ... # type:ignore[assignment,unused-ignore]

class ReadableStreamReadResult__Union1(Protocol): # type:ignore[misc, unused-ignore]
    done: Literal[True] = ... # type:ignore[assignment,unused-ignore]
    value: None = ... # type:ignore[assignment,unused-ignore]

class AiImageClassificationInput(Protocol): # type:ignore[misc, unused-ignore]
    image: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class AiImageClassificationOutput__array(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]
    label: str | None = ... # type:ignore[assignment,unused-ignore]

class AiImageToTextInput(Protocol): # type:ignore[misc, unused-ignore]
    image: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]
    prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    messages: JsArray[RoleScopedChatInput] | None = ... # type:ignore[assignment,unused-ignore]

class AiImageToTextOutput(Protocol): # type:ignore[misc, unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]

class AiImageTextToTextInput(Protocol): # type:ignore[misc, unused-ignore]
    image: str = ... # type:ignore[assignment,unused-ignore]
    prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    ignore_eos: bool | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    messages: JsArray[RoleScopedChatInput] | None = ... # type:ignore[assignment,unused-ignore]

class AiImageTextToTextOutput(Protocol): # type:ignore[misc, unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]

class AiObjectDetectionInput(Protocol): # type:ignore[misc, unused-ignore]
    image: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class AiObjectDetectionOutput__array(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]
    label: str | None = ... # type:ignore[assignment,unused-ignore]

class AiSentenceSimilarityInput(Protocol): # type:ignore[misc, unused-ignore]
    source: str = ... # type:ignore[assignment,unused-ignore]
    sentences: JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class AiAutomaticSpeechRecognitionInput(Protocol): # type:ignore[misc, unused-ignore]
    audio: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class AiAutomaticSpeechRecognitionOutput__words__array(Protocol): # type:ignore[misc, unused-ignore]
    word: str = ... # type:ignore[assignment,unused-ignore]
    start: int | float = ... # type:ignore[assignment,unused-ignore]
    end: int | float = ... # type:ignore[assignment,unused-ignore]

class AiAutomaticSpeechRecognitionOutput(Protocol): # type:ignore[misc, unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[AiAutomaticSpeechRecognitionOutput__words__array] | None = ... # type:ignore[assignment,unused-ignore]
    vtt: str | None = ... # type:ignore[assignment,unused-ignore]

class AiSummarizationInput(Protocol): # type:ignore[misc, unused-ignore]
    input_text: str = ... # type:ignore[assignment,unused-ignore]
    max_length: int | float | None = ... # type:ignore[assignment,unused-ignore]

class AiSummarizationOutput(Protocol): # type:ignore[misc, unused-ignore]
    summary: str = ... # type:ignore[assignment,unused-ignore]

class AiTextClassificationInput(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]

class AiTextClassificationOutput__array(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]
    label: str | None = ... # type:ignore[assignment,unused-ignore]

class AiTextEmbeddingsInput(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class AiTextEmbeddingsOutput(Protocol): # type:ignore[misc, unused-ignore]
    shape: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[JsArray[int | float]] = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationInput__tools__Union2(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationInput(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    messages: JsArray[RoleScopedChatInput] | None = ... # type:ignore[assignment,unused-ignore]
    response_format: AiTextGenerationResponseFormat | None = ... # type:ignore[assignment,unused-ignore]
    tools: JsArray[AiTextGenerationToolInput] | JsArray[AiTextGenerationToolLegacyInput] | (AiTextGenerationInput__tools__Union2) | None = ... # type:ignore[assignment,unused-ignore]
    functions: JsArray[AiTextGenerationFunctionsInput] | None = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationOutput__tool_calls(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationOutput(Protocol): # type:ignore[misc, unused-ignore]
    response: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: AiTextGenerationOutput__tool_calls | None = ... # type:ignore[assignment,unused-ignore]
    usage: UsageTags | None = ... # type:ignore[assignment,unused-ignore]

class AiTextToSpeechInput(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    lang: str | None = ... # type:ignore[assignment,unused-ignore]

class AiTextToSpeechOutput__Union1(Protocol): # type:ignore[misc, unused-ignore]
    audio: str = ... # type:ignore[assignment,unused-ignore]

class AiTextToImageInput(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str = ... # type:ignore[assignment,unused-ignore]
    negative_prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    height: int | float | None = ... # type:ignore[assignment,unused-ignore]
    width: int | float | None = ... # type:ignore[assignment,unused-ignore]
    image: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    image_b64: str | None = ... # type:ignore[assignment,unused-ignore]
    mask: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    num_steps: int | float | None = ... # type:ignore[assignment,unused-ignore]
    strength: int | float | None = ... # type:ignore[assignment,unused-ignore]
    guidance: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]

class AiTranslationInput(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    target_lang: str = ... # type:ignore[assignment,unused-ignore]
    source_lang: str | None = ... # type:ignore[assignment,unused-ignore]

class AiTranslationOutput(Protocol): # type:ignore[misc, unused-ignore]
    translated_text: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union0(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union1__requests__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[Ai_Cf_Baai_Bge_Base_En_V1_5_Input__Union1__requests__array] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Base_En_V1_5_Output__Union0(Protocol): # type:ignore[misc, unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    audio: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Output_iface__words__array(Protocol): # type:ignore[misc, unused-ignore]
    word: str | None = ... # type:ignore[assignment,unused-ignore]
    start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_M2M100_1_2B_Input__Union0(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    source_lang: str | None = ... # type:ignore[assignment,unused-ignore]
    target_lang: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_M2M100_1_2B_Input__Union1__requests__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    source_lang: str | None = ... # type:ignore[assignment,unused-ignore]
    target_lang: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_M2M100_1_2B_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[Ai_Cf_Meta_M2M100_1_2B_Input__Union1__requests__array] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_M2M100_1_2B_Output__Union0(Protocol): # type:ignore[misc, unused-ignore]
    translated_text: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union0(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union1__requests__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[Ai_Cf_Baai_Bge_Small_En_V1_5_Input__Union1__requests__array] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Small_En_V1_5_Output__Union0(Protocol): # type:ignore[misc, unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union0(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union1__requests__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[Ai_Cf_Baai_Bge_Large_En_V1_5_Input__Union1__requests__array] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Large_En_V1_5_Output__Union0(Protocol): # type:ignore[misc, unused-ignore]
    shape: JsArray[int | float] | None = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[JsArray[int | float]] | None = ... # type:ignore[assignment,unused-ignore]
    pooling: Literal["mean", "cls"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input__Union1__image__Union1(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    raw: bool | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_k: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    image: JsArray[int | float] | (Ai_Cf_Unum_Uform_Gen2_Qwen_500M_Input__Union1__image__Union1) = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Tiny_En_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    audio: JsArray[int | float] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Tiny_En_Output_iface__words__array(Protocol): # type:ignore[misc, unused-ignore]
    word: str | None = ... # type:ignore[assignment,unused-ignore]
    start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__transcription_info(Protocol): # type:ignore[misc, unused-ignore]
    language: str | None = ... # type:ignore[assignment,unused-ignore]
    language_probability: int | float | None = ... # type:ignore[assignment,unused-ignore]
    duration: int | float | None = ... # type:ignore[assignment,unused-ignore]
    duration_after_vad: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__segments__array__words__array(Protocol): # type:ignore[misc, unused-ignore]
    word: str | None = ... # type:ignore[assignment,unused-ignore]
    start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__segments__array(Protocol): # type:ignore[misc, unused-ignore]
    start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end: int | float | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    avg_logprob: int | float | None = ... # type:ignore[assignment,unused-ignore]
    compression_ratio: int | float | None = ... # type:ignore[assignment,unused-ignore]
    no_speech_prob: int | float | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[Ai_Cf_Openai_Whisper_Large_V3_Turbo_Output_iface__segments__array__words__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input__Union2(Protocol): # type:ignore[misc, unused-ignore]
    requests: JsArray[(Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_1_iface | Ai_Cf_Baai_Bge_M3_Input_Embedding_1_iface)] = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Output__Union0__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: Literal["user", "assistant"] = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Input_iface__response_format(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface__response__Union1(Protocol): # type:ignore[misc, unused-ignore]
    safe: bool | None = ... # type:ignore[assignment,unused-ignore]
    categories: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_Guard_3_8B_Output_iface__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Reranker_Base_Input_iface__contexts__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_Reranker_Base_Output_iface__response__array(Protocol): # type:ignore[misc, unused-ignore]
    id: int | float | None = ... # type:ignore[assignment,unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Output__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Qwen_Qwq_32B_Output__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Qwen_Qwq_32B_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Output__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Google_Gemma_3_12B_It_Output__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Google_Gemma_3_12B_It_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__tool_calls__array__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]
    arguments: Any | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__tool_calls__array__function | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]
    usage: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__usage | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Output__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Input_iface__audio(Protocol): # type:ignore[misc, unused-ignore]
    body: Any = ... # type:ignore[assignment,unused-ignore]
    contentType: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array__alternatives__array__words__array(Protocol): # type:ignore[misc, unused-ignore]
    confidence: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end: int | float | None = ... # type:ignore[assignment,unused-ignore]
    start: int | float | None = ... # type:ignore[assignment,unused-ignore]
    word: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array__alternatives__array(Protocol): # type:ignore[misc, unused-ignore]
    confidence: int | float | None = ... # type:ignore[assignment,unused-ignore]
    transcript: str | None = ... # type:ignore[assignment,unused-ignore]
    words: JsArray[Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array__alternatives__array__words__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array(Protocol): # type:ignore[misc, unused-ignore]
    alternatives: JsArray[Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array__alternatives__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__summary(Protocol): # type:ignore[misc, unused-ignore]
    result: str | None = ... # type:ignore[assignment,unused-ignore]
    short: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments__segments__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    start_word: int | float | None = ... # type:ignore[assignment,unused-ignore]
    end_word: int | float | None = ... # type:ignore[assignment,unused-ignore]
    sentiment: str | None = ... # type:ignore[assignment,unused-ignore]
    sentiment_score: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments__average(Protocol): # type:ignore[misc, unused-ignore]
    sentiment: str | None = ... # type:ignore[assignment,unused-ignore]
    sentiment_score: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments(Protocol): # type:ignore[misc, unused-ignore]
    segments: JsArray[Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments__segments__array] | None = ... # type:ignore[assignment,unused-ignore]
    average: Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments__average | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Nova_3_Output_iface__results(Protocol): # type:ignore[misc, unused-ignore]
    channels: JsArray[Ai_Cf_Deepgram_Nova_3_Output_iface__results__channels__array] | None = ... # type:ignore[assignment,unused-ignore]
    summary: Ai_Cf_Deepgram_Nova_3_Output_iface__results__summary | None = ... # type:ignore[assignment,unused-ignore]
    sentiments: Ai_Cf_Deepgram_Nova_3_Output_iface__results__sentiments | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union0__audio(Protocol): # type:ignore[misc, unused-ignore]
    body: Any = ... # type:ignore[assignment,unused-ignore]
    contentType: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union0(Protocol): # type:ignore[misc, unused-ignore]
    audio: Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union0__audio = ... # type:ignore[assignment,unused-ignore]
    dtype: Literal["uint8", "float32", "float64"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Pipecat_Ai_Smart_Turn_V2_Input__Union1(Protocol): # type:ignore[misc, unused-ignore]
    audio: str = ... # type:ignore[assignment,unused-ignore]
    dtype: Literal["uint8", "float32", "float64"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponsesInput(Protocol): # type:ignore[misc, unused-ignore]
    background: bool | None = ... # type:ignore[assignment,unused-ignore]
    conversation: str | ResponseConversationParam | None = ... # type:ignore[assignment,unused-ignore]
    include: ArrayLike_iface[ResponseIncludable] | None = ... # type:ignore[assignment,unused-ignore]
    input: str | ResponseInput | None = ... # type:ignore[assignment,unused-ignore]
    instructions: str | None = ... # type:ignore[assignment,unused-ignore]
    max_output_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    parallel_tool_calls: bool | None = ... # type:ignore[assignment,unused-ignore]
    previous_response_id: str | None = ... # type:ignore[assignment,unused-ignore]
    prompt_cache_key: str | None = ... # type:ignore[assignment,unused-ignore]
    reasoning: Reasoning | None = ... # type:ignore[assignment,unused-ignore]
    safety_identifier: str | None = ... # type:ignore[assignment,unused-ignore]
    Literal["auto", "default", "flex", "scale", "priority"] | None
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    stream_options: StreamOptions | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    text: ResponseTextConfig | None = ... # type:ignore[assignment,unused-ignore]
    tool_choice: ToolChoiceOptions | ToolChoiceFunction | None = ... # type:ignore[assignment,unused-ignore]
    tools: ArrayLike_iface[Tool] | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    truncation: Literal["auto", "disabled"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponsesOutput(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    created_at: int | float | None = ... # type:ignore[assignment,unused-ignore]
    output_text: str | None = ... # type:ignore[assignment,unused-ignore]
    error: ResponseError | None = ... # type:ignore[assignment,unused-ignore]
    incomplete_details: ResponseIncompleteDetails | None = ... # type:ignore[assignment,unused-ignore]
    instructions: str | ArrayLike_iface[ResponseInputItem] | None = ... # type:ignore[assignment,unused-ignore]
    object: Literal["response"] | None = ... # type:ignore[assignment,unused-ignore]
    output: ArrayLike_iface[ResponseOutputItem] | None = ... # type:ignore[assignment,unused-ignore]
    parallel_tool_calls: bool | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    tool_choice: ToolChoiceOptions | ToolChoiceFunction | None = ... # type:ignore[assignment,unused-ignore]
    tools: ArrayLike_iface[Tool] | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    max_output_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    previous_response_id: str | None = ... # type:ignore[assignment,unused-ignore]
    prompt: ResponsePrompt | None = ... # type:ignore[assignment,unused-ignore]
    reasoning: Reasoning | None = ... # type:ignore[assignment,unused-ignore]
    safety_identifier: str | None = ... # type:ignore[assignment,unused-ignore]
    Literal["auto", "default", "flex", "scale", "priority"] | None
    status: ResponseStatus | None = ... # type:ignore[assignment,unused-ignore]
    text: ResponseTextConfig | None = ... # type:ignore[assignment,unused-ignore]
    truncation: Literal["auto", "disabled"] | None = ... # type:ignore[assignment,unused-ignore]
    usage: ResponseUsage | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Deepgram_Flux_Output_iface__words__array(Protocol): # type:ignore[misc, unused-ignore]
    word: str = ... # type:ignore[assignment,unused-ignore]
    confidence: int | float = ... # type:ignore[assignment,unused-ignore]

class AiModelsSearchParams(Protocol): # type:ignore[misc, unused-ignore]
    author: str | None = ... # type:ignore[assignment,unused-ignore]
    hide_experimental: bool | None = ... # type:ignore[assignment,unused-ignore]
    page: int | float | None = ... # type:ignore[assignment,unused-ignore]
    per_page: int | float | None = ... # type:ignore[assignment,unused-ignore]
    search: str | None = ... # type:ignore[assignment,unused-ignore]
    source: int | float | None = ... # type:ignore[assignment,unused-ignore]
    task: str | None = ... # type:ignore[assignment,unused-ignore]

class AiModelsSearchObject__task(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]

class AiModelsSearchObject__properties__array(Protocol): # type:ignore[misc, unused-ignore]
    property_id: str = ... # type:ignore[assignment,unused-ignore]
    value: str = ... # type:ignore[assignment,unused-ignore]

class AiModelsSearchObject(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    source: int | float = ... # type:ignore[assignment,unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    task: AiModelsSearchObject__task = ... # type:ignore[assignment,unused-ignore]
    tags: JsArray[str] = ... # type:ignore[assignment,unused-ignore]
    properties: JsArray[AiModelsSearchObject__properties__array] = ... # type:ignore[assignment,unused-ignore]

class MarkdownDocument(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    blob: Blob = ... # type:ignore[assignment,unused-ignore]

class ConversionRequestOptions(Protocol): # type:ignore[misc, unused-ignore]
    gateway: GatewayOptions | None = ... # type:ignore[assignment,unused-ignore]
    extraHeaders: Any | None = ... # type:ignore[assignment,unused-ignore]
    conversionOptions: ConversionOptions | None = ... # type:ignore[assignment,unused-ignore]

class ConversionResponse__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    mimeType: str = ... # type:ignore[assignment,unused-ignore]
    format: Literal['markdown'] = ... # type:ignore[assignment,unused-ignore]
    tokens: int | float = ... # type:ignore[assignment,unused-ignore]
    data: str = ... # type:ignore[assignment,unused-ignore]

class ConversionResponse__Union1(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    mimeType: str = ... # type:ignore[assignment,unused-ignore]
    format: Literal['error'] = ... # type:ignore[assignment,unused-ignore]
    error: str = ... # type:ignore[assignment,unused-ignore]

class AiGatewayPatchLog(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]
    feedback: Literal[-1, 1] | None = ... # type:ignore[assignment,unused-ignore]
    metadata: Record[str, int | float | str | bool | int | None] | None = ... # type:ignore[assignment,unused-ignore]

class AiGatewayLog(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    provider: str = ... # type:ignore[assignment,unused-ignore]
    model: str = ... # type:ignore[assignment,unused-ignore]
    model_type: str | None = ... # type:ignore[assignment,unused-ignore]
    path: str = ... # type:ignore[assignment,unused-ignore]
    duration: int | float = ... # type:ignore[assignment,unused-ignore]
    request_type: str | None = ... # type:ignore[assignment,unused-ignore]
    request_content_type: str | None = ... # type:ignore[assignment,unused-ignore]
    status_code: int | float = ... # type:ignore[assignment,unused-ignore]
    response_content_type: str | None = ... # type:ignore[assignment,unused-ignore]
    success: bool = ... # type:ignore[assignment,unused-ignore]
    cached: bool = ... # type:ignore[assignment,unused-ignore]
    tokens_in: int | float | None = ... # type:ignore[assignment,unused-ignore]
    tokens_out: int | float | None = ... # type:ignore[assignment,unused-ignore]
    metadata: Record[str, int | float | str | bool | int | None] | None = ... # type:ignore[assignment,unused-ignore]
    step: int | float | None = ... # type:ignore[assignment,unused-ignore]
    cost: int | float | None = ... # type:ignore[assignment,unused-ignore]
    custom_cost: bool | None = ... # type:ignore[assignment,unused-ignore]
    request_size: int | float = ... # type:ignore[assignment,unused-ignore]
    request_head: str | None = ... # type:ignore[assignment,unused-ignore]
    request_head_complete: bool = ... # type:ignore[assignment,unused-ignore]
    response_size: int | float = ... # type:ignore[assignment,unused-ignore]
    response_head: str | None = ... # type:ignore[assignment,unused-ignore]
    response_head_complete: bool = ... # type:ignore[assignment,unused-ignore]
    created_at: Date = ... # type:ignore[assignment,unused-ignore]

class AIGatewayUniversalRequest__headers__Partial(Protocol): # type:ignore[misc, unused-ignore]
    Authorization: str | None = ... # type:ignore[assignment,unused-ignore]

class AIGatewayUniversalRequest(Protocol): # type:ignore[misc, unused-ignore]
    provider: AIGatewayProviders | str = ... # type:ignore[assignment,unused-ignore]
    endpoint: str = ... # type:ignore[assignment,unused-ignore]
    headers: AIGatewayUniversalRequest__headers__Partial = ... # type:ignore[assignment,unused-ignore]
    query: Any = ... # type:ignore[assignment,unused-ignore]

class UniversalGatewayOptions__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]

class UniversalGatewayOptions(UniversalGatewayOptions__Intersection1, Protocol): # type:ignore[misc, unused-ignore]
    pass

class AutoRagListResponse__array(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    enable: bool = ... # type:ignore[assignment,unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    source: str = ... # type:ignore[assignment,unused-ignore]
    vectorize_name: str = ... # type:ignore[assignment,unused-ignore]
    paused: bool = ... # type:ignore[assignment,unused-ignore]
    status: str = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchRequest__ranking_options(Protocol): # type:ignore[misc, unused-ignore]
    ranker: str | None = ... # type:ignore[assignment,unused-ignore]
    score_threshold: int | float | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchRequest__reranking(Protocol): # type:ignore[misc, unused-ignore]
    enabled: bool | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchRequest(Protocol): # type:ignore[misc, unused-ignore]
    query: str = ... # type:ignore[assignment,unused-ignore]
    filters: CompoundFilter | ComparisonFilter | None = ... # type:ignore[assignment,unused-ignore]
    max_num_results: int | float | None = ... # type:ignore[assignment,unused-ignore]
    ranking_options: AutoRagSearchRequest__ranking_options | None = ... # type:ignore[assignment,unused-ignore]
    reranking: AutoRagSearchRequest__reranking | None = ... # type:ignore[assignment,unused-ignore]
    rewrite_query: bool | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchResponse__data__array__content__array(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal['text'] = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchResponse__data__array(Protocol): # type:ignore[misc, unused-ignore]
    file_id: str = ... # type:ignore[assignment,unused-ignore]
    filename: str = ... # type:ignore[assignment,unused-ignore]
    score: int | float = ... # type:ignore[assignment,unused-ignore]
    attributes: Record[str, str | int | float | bool | None] = ... # type:ignore[assignment,unused-ignore]
    content: JsArray[AutoRagSearchResponse__data__array__content__array] = ... # type:ignore[assignment,unused-ignore]

class AutoRagSearchResponse(Protocol): # type:ignore[misc, unused-ignore]
    object: Literal['vector_store.search_results.page'] = ... # type:ignore[assignment,unused-ignore]
    search_query: str = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[AutoRagSearchResponse__data__array] = ... # type:ignore[assignment,unused-ignore]
    has_more: bool = ... # type:ignore[assignment,unused-ignore]
    next_page: str | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequestStreaming__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    stream: Literal[True] = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequestStreaming(AutoRagAiSearchRequestStreaming__Intersection1, Protocol): # type:ignore[misc, unused-ignore]
    pass

class AutoRagAiSearchRequest__Intersection0__ranking_options(Protocol): # type:ignore[misc, unused-ignore]
    ranker: str | None = ... # type:ignore[assignment,unused-ignore]
    score_threshold: int | float | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequest__Intersection0__reranking(Protocol): # type:ignore[misc, unused-ignore]
    enabled: bool | None = ... # type:ignore[assignment,unused-ignore]
    model: str | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequest__Intersection0(Protocol): # type:ignore[misc, unused-ignore]
    query: str = ... # type:ignore[assignment,unused-ignore]
    filters: CompoundFilter | ComparisonFilter | None = ... # type:ignore[assignment,unused-ignore]
    max_num_results: int | float | None = ... # type:ignore[assignment,unused-ignore]
    ranking_options: AutoRagAiSearchRequest__Intersection0__ranking_options | None = ... # type:ignore[assignment,unused-ignore]
    reranking: AutoRagAiSearchRequest__Intersection0__reranking | None = ... # type:ignore[assignment,unused-ignore]
    rewrite_query: bool | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequest__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    system_prompt: str | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchRequest(AutoRagAiSearchRequest__Intersection1, AutoRagAiSearchRequest__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class AutoRagAiSearchResponse__Intersection0__data__array__content__array(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal['text'] = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchResponse__Intersection0__data__array(Protocol): # type:ignore[misc, unused-ignore]
    file_id: str = ... # type:ignore[assignment,unused-ignore]
    filename: str = ... # type:ignore[assignment,unused-ignore]
    score: int | float = ... # type:ignore[assignment,unused-ignore]
    attributes: Record[str, str | int | float | bool | None] = ... # type:ignore[assignment,unused-ignore]
    content: JsArray[AutoRagAiSearchResponse__Intersection0__data__array__content__array] = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchResponse__Intersection0(Protocol): # type:ignore[misc, unused-ignore]
    object: Literal['vector_store.search_results.page'] = ... # type:ignore[assignment,unused-ignore]
    search_query: str = ... # type:ignore[assignment,unused-ignore]
    data: JsArray[AutoRagAiSearchResponse__Intersection0__data__array] = ... # type:ignore[assignment,unused-ignore]
    has_more: bool = ... # type:ignore[assignment,unused-ignore]
    next_page: str | None = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchResponse__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    response: str = ... # type:ignore[assignment,unused-ignore]

class AutoRagAiSearchResponse(AutoRagAiSearchResponse__Intersection1, AutoRagAiSearchResponse__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class D1Result__Intersection1[T](Protocol): # type:ignore[misc, unused-ignore]
    results: JsArray[T] = ... # type:ignore[assignment,unused-ignore]

class D1Result[T=Any](D1Result__Intersection1[T], D1Response_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class SupportedFileFormat(Protocol): # type:ignore[misc, unused-ignore]
    mimeType: str = ... # type:ignore[assignment,unused-ignore]
    extension: str = ... # type:ignore[assignment,unused-ignore]

class VectorizeVectorMetadataFilter(Protocol): # type:ignore[misc, unused-ignore]
    pass

class WorkflowInstanceCreateOptions_iface__retention(Protocol): # type:ignore[misc, unused-ignore]
    successRetention: WorkflowRetentionDuration | None = ... # type:ignore[assignment,unused-ignore]
    errorRetention: WorkflowRetentionDuration | None = ... # type:ignore[assignment,unused-ignore]

class InstanceStatus__error(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    message: str = ... # type:ignore[assignment,unused-ignore]

class InstanceStatus(Protocol): # type:ignore[misc, unused-ignore]
    status: Literal['queued', 'running', 'paused', 'errored', 'terminated', 'complete', 'waiting', 'waitingForPause', 'unknown'] = ... # type:ignore[assignment,unused-ignore]
    error: InstanceStatus__error | None = ... # type:ignore[assignment,unused-ignore]
    output: Any | None = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfProperties[HostMetadata=Any](IncomingRequestCfPropertiesCloudflareAccessOrApiShield_iface, IncomingRequestCfPropertiesGeographicInformation_iface, IncomingRequestCfPropertiesCloudflareForSaaSEnterprise_iface[HostMetadata], IncomingRequestCfPropertiesBotManagementEnterprise_iface, IncomingRequestCfPropertiesBase_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class RequestInitCfPropertiesImage_iface__trim__Union0__border__Union1(Protocol): # type:ignore[misc, unused-ignore]
    color: str | None = ... # type:ignore[assignment,unused-ignore]
    tolerance: int | float | None = ... # type:ignore[assignment,unused-ignore]
    keep: int | float | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImage_iface__trim__Union0(Protocol): # type:ignore[misc, unused-ignore]
    top: int | float | None = ... # type:ignore[assignment,unused-ignore]
    bottom: int | float | None = ... # type:ignore[assignment,unused-ignore]
    left: int | float | None = ... # type:ignore[assignment,unused-ignore]
    right: int | float | None = ... # type:ignore[assignment,unused-ignore]
    width: int | float | None = ... # type:ignore[assignment,unused-ignore]
    height: int | float | None = ... # type:ignore[assignment,unused-ignore]
    border: bool | RequestInitCfPropertiesImage_iface__trim__Union0__border__Union1 | None = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImage_iface__border__Union0(Protocol): # type:ignore[misc, unused-ignore]
    color: str = ... # type:ignore[assignment,unused-ignore]
    width: int | float = ... # type:ignore[assignment,unused-ignore]

class RequestInitCfPropertiesImage_iface__border__Union1(Protocol): # type:ignore[misc, unused-ignore]
    color: str = ... # type:ignore[assignment,unused-ignore]
    top: int | float = ... # type:ignore[assignment,unused-ignore]
    right: int | float = ... # type:ignore[assignment,unused-ignore]
    bottom: int | float = ... # type:ignore[assignment,unused-ignore]
    left: int | float = ... # type:ignore[assignment,unused-ignore]

class WebSocketEventMap(Protocol): # type:ignore[misc, unused-ignore]
    close: CloseEvent = ... # type:ignore[assignment,unused-ignore]
    message: MessageEvent = ... # type:ignore[assignment,unused-ignore]
    open: Event = ... # type:ignore[assignment,unused-ignore]
    error: ErrorEvent = ... # type:ignore[assignment,unused-ignore]

class RegExpMatchArray_iface__groups(Protocol): # type:ignore[misc, unused-ignore]
    pass

class RegExpExecArray_iface__groups(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Element_iface__onEndTag__Sig0__handler(Protocol): # type:ignore[misc, unused-ignore]
    @overload
    def __call__(self, tag: EndTag_iface, /) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]
    @overload
    def __call__(self, /, *, name: str) -> None | Future[None]: ... # type:ignore[misc,overload-overlap,override,unused-ignore]

class RoleScopedChatInput__role__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class RoleScopedChatInput(Protocol): # type:ignore[misc, unused-ignore]
    role: (RoleScopedChatInput__role__Union0) | Literal["user", "assistant", "system", "tool"] = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]
    name: str | None = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationResponseFormat(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    json_schema: Any | None = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolInput__type__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationToolInput__function__parameters__type__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationToolInput__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationToolInput__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: (AiTextGenerationToolInput__function__parameters__type__Union0) | Literal["object"] = ... # type:ignore[assignment,unused-ignore]
    properties: AiTextGenerationToolInput__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolInput__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: AiTextGenerationToolInput__function__parameters | None = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolInput(Protocol): # type:ignore[misc, unused-ignore]
    type: (AiTextGenerationToolInput__type__Union0) | Literal["function"] = ... # type:ignore[assignment,unused-ignore]
    function: AiTextGenerationToolInput__function = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolLegacyInput__parameters__type__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationToolLegacyInput__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class AiTextGenerationToolLegacyInput__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: (AiTextGenerationToolLegacyInput__parameters__type__Union0) | Literal["object"] = ... # type:ignore[assignment,unused-ignore]
    properties: AiTextGenerationToolLegacyInput__parameters__properties = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolLegacyInput(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: AiTextGenerationToolLegacyInput__parameters | None = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationFunctionsInput(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolLegacyOutput(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    arguments: Any = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolOutput__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    arguments: str = ... # type:ignore[assignment,unused-ignore]

class AiTextGenerationToolOutput(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function"] = ... # type:ignore[assignment,unused-ignore]
    function: AiTextGenerationToolOutput__function = ... # type:ignore[assignment,unused-ignore]

class UsageTags(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_iface__contexts__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Input_QueryAnd_Contexts_1_iface__contexts__array(Protocol): # type:ignore[misc, unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Baai_Bge_M3_Ouput_Query_iface__response__array(Protocol): # type:ignore[misc, unused-ignore]
    id: int | float | None = ... # type:ignore[assignment,unused-ignore]
    score: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Prompt_iface__image__Union1(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union2__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union2(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union2__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_call_id: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union1__array] | Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__messages__array__content__Union2 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__image__Union1(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Meta_Llama_3_2_11B_Vision_Instruct_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_Async_Batch_iface__requests__array(Protocol): # type:ignore[misc, unused-ignore]
    external_reference: str | None = ... # type:ignore[assignment,unused-ignore]
    prompt: str | None = ... # type:ignore[assignment,unused-ignore]
    stream: bool | None = ... # type:ignore[assignment,unused-ignore]
    max_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    temperature: int | float | None = ... # type:ignore[assignment,unused-ignore]
    top_p: int | float | None = ... # type:ignore[assignment,unused-ignore]
    seed: int | float | None = ... # type:ignore[assignment,unused-ignore]
    repetition_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    frequency_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    presence_penalty: int | float | None = ... # type:ignore[assignment,unused-ignore]
    response_format: Ai_Cf_Meta_Llama_3_3_70B_Instruct_Fp8_Fast_JSON_Mode_2_iface | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Qwen_Qwen2_5_Coder_32B_Instruct_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union2__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union2(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union2__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_call_id: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union1__array] | Ai_Cf_Qwen_Qwq_32B_Messages_iface__messages__array__content__Union2 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Qwen_Qwq_32B_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union2__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union2(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union2__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_call_id: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union1__array] | Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__messages__array__content__Union2 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Mistralai_Mistral_Small_3_1_24B_Instruct_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__messages__array__content__Union1__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Google_Gemma_3_12B_It_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union2__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union2(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union2__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_call_id: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union1__array] | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__messages__array__content__Union2 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message__tool_calls__array__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    arguments: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function"] = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message__tool_calls__array__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]
    reasoning_content: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array(Protocol): # type:ignore[misc, unused-ignore]
    index: int | float | None = ... # type:ignore[assignment,unused-ignore]
    message: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__message | None = ... # type:ignore[assignment,unused-ignore]
    finish_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    stop_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    logprobs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__choices__array__logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Chat_Completion_Response_iface__prompt_logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array__logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array__prompt_logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array(Protocol): # type:ignore[misc, unused-ignore]
    index: int | float = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    finish_reason: str = ... # type:ignore[assignment,unused-ignore]
    stop_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    logprobs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array__logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]
    prompt_logprobs: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__choices__array__prompt_logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Text_Completion_Response_iface__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class ResponseConversationParam(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]

class Reasoning(Protocol): # type:ignore[misc, unused-ignore]
    effort: ReasoningEffort | None = ... # type:ignore[assignment,unused-ignore]
    generate_summary: Literal["auto", "concise", "detailed"] | None = ... # type:ignore[assignment,unused-ignore]
    summary: Literal["auto", "concise", "detailed"] | None = ... # type:ignore[assignment,unused-ignore]

class StreamOptions(Protocol): # type:ignore[misc, unused-ignore]
    include_obfuscation: bool | None = ... # type:ignore[assignment,unused-ignore]

class ResponseTextConfig(Protocol): # type:ignore[misc, unused-ignore]
    format: ResponseFormatTextConfig | None = ... # type:ignore[assignment,unused-ignore]
    verbosity: Literal["low", "medium", "high"] | None = ... # type:ignore[assignment,unused-ignore]

class ToolChoiceFunction(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function"] = ... # type:ignore[assignment,unused-ignore]

class ResponseError(Protocol): # type:ignore[misc, unused-ignore]
    code: Literal["server_error", "rate_limit_exceeded", "invalid_prompt", "vector_store_timeout", "invalid_image", "invalid_image_format", "invalid_base64_image", "invalid_image_url", "image_too_large", "image_too_small", "image_parse_error", "image_content_policy_violation", "invalid_image_mode", "image_file_too_large", "unsupported_image_media_type", "empty_image_file", "failed_to_download_image", "image_file_not_found"] = ... # type:ignore[assignment,unused-ignore]
    message: str = ... # type:ignore[assignment,unused-ignore]

class ResponseIncompleteDetails(Protocol): # type:ignore[misc, unused-ignore]
    reason: Literal["max_output_tokens", "content_filter"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponsePrompt__variables__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ResponsePrompt(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    variables: ResponsePrompt__variables__Union0 | None = ... # type:ignore[assignment,unused-ignore]
    version: str | None = ... # type:ignore[assignment,unused-ignore]

class ResponseUsage(Protocol): # type:ignore[misc, unused-ignore]
    input_tokens: int | float = ... # type:ignore[assignment,unused-ignore]
    output_tokens: int | float = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message__tool_calls__array__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    arguments: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message__tool_calls__array(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function"] = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message__tool_calls__array__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]
    reasoning_content: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_calls: JsArray[Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message__tool_calls__array] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array(Protocol): # type:ignore[misc, unused-ignore]
    index: int | float | None = ... # type:ignore[assignment,unused-ignore]
    message: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__message | None = ... # type:ignore[assignment,unused-ignore]
    finish_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    stop_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    logprobs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__choices__array__logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Chat_Completion_Response_iface__prompt_logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array__logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array__prompt_logprobs__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array(Protocol): # type:ignore[misc, unused-ignore]
    index: int | float = ... # type:ignore[assignment,unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    finish_reason: str = ... # type:ignore[assignment,unused-ignore]
    stop_reason: str | None = ... # type:ignore[assignment,unused-ignore]
    logprobs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array__logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]
    prompt_logprobs: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__choices__array__prompt_logprobs__Union0 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Text_Completion_Response_iface__usage(Protocol): # type:ignore[misc, unused-ignore]
    prompt_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    completion_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]
    total_tokens: int | float | None = ... # type:ignore[assignment,unused-ignore]

class GatewayOptions(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    cacheKey: str | None = ... # type:ignore[assignment,unused-ignore]
    cacheTtl: int | float | None = ... # type:ignore[assignment,unused-ignore]
    skipCache: bool | None = ... # type:ignore[assignment,unused-ignore]
    metadata: Record[str, int | float | str | bool | int | None] | None = ... # type:ignore[assignment,unused-ignore]
    collectLog: bool | None = ... # type:ignore[assignment,unused-ignore]
    eventId: str | None = ... # type:ignore[assignment,unused-ignore]
    requestTimeoutMs: int | float | None = ... # type:ignore[assignment,unused-ignore]
    retries: GatewayRetries | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__html__images__Intersection0__Intersection0(Protocol): # type:ignore[misc, unused-ignore]
    descriptionLanguage: Literal['en', 'es', 'fr', 'it', 'pt', 'de'] | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__html__images__Intersection0__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    convert: bool | None = ... # type:ignore[assignment,unused-ignore]
    maxConvertedImages: int | float | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__html__images__Intersection0(ConversionOptions__html__images__Intersection0__Intersection1, ConversionOptions__html__images__Intersection0__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ConversionOptions__html__images__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    convertOGImage: bool | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__html__images(ConversionOptions__html__images__Intersection1, ConversionOptions__html__images__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ConversionOptions__html(Protocol): # type:ignore[misc, unused-ignore]
    images: ConversionOptions__html__images | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__docx(Protocol): # type:ignore[misc, unused-ignore]
    images: EmbeddedImageConversionOptions | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions__pdf(Protocol): # type:ignore[misc, unused-ignore]
    images: EmbeddedImageConversionOptions | None = ... # type:ignore[assignment,unused-ignore]
    metadata: bool | None = ... # type:ignore[assignment,unused-ignore]

class ConversionOptions(Protocol): # type:ignore[misc, unused-ignore]
    html: ConversionOptions__html | None = ... # type:ignore[assignment,unused-ignore]
    docx: ConversionOptions__docx | None = ... # type:ignore[assignment,unused-ignore]
    image: ImageConversionOptions | None = ... # type:ignore[assignment,unused-ignore]
    pdf: ConversionOptions__pdf | None = ... # type:ignore[assignment,unused-ignore]

class CompoundFilter(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal['and', 'or'] = ... # type:ignore[assignment,unused-ignore]
    filters: JsArray[ComparisonFilter] = ... # type:ignore[assignment,unused-ignore]

class ComparisonFilter(Protocol): # type:ignore[misc, unused-ignore]
    key: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal['eq', 'ne', 'gt', 'gte', 'lt', 'lte'] = ... # type:ignore[assignment,unused-ignore]
    value: str | int | float | bool = ... # type:ignore[assignment,unused-ignore]

class D1Response_iface__meta(D1Meta_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class VectorizeIndexConfig__Union0(Protocol): # type:ignore[misc, unused-ignore]
    dimensions: int | float = ... # type:ignore[assignment,unused-ignore]
    metric: VectorizeDistanceMetric = ... # type:ignore[assignment,unused-ignore]

class VectorizeIndexConfig__Union1(Protocol): # type:ignore[misc, unused-ignore]
    preset: str = ... # type:ignore[assignment,unused-ignore]

class VectorizeMatch__Intersection2(Protocol): # type:ignore[misc, unused-ignore]
    score: int | float = ... # type:ignore[assignment,unused-ignore]

class VectorizeMatch(VectorizeMatch__Intersection2, Protocol): # type:ignore[misc, unused-ignore]
    pass

class IncomingRequestCfPropertiesBotManagementEnterprise_iface__botManagement__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    ja3Hash: str = ... # type:ignore[assignment,unused-ignore]

class IncomingRequestCfPropertiesBotManagementEnterprise_iface__botManagement(IncomingRequestCfPropertiesBotManagementEnterprise_iface__botManagement__Intersection1, IncomingRequestCfPropertiesBotManagementBase_iface, Protocol): # type:ignore[misc, unused-ignore]
    pass

class RegExpIndicesArray_iface__groups(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union1__array__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union1__array(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union1__array__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union2__image_url(Protocol): # type:ignore[misc, unused-ignore]
    url: str | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union2(Protocol): # type:ignore[misc, unused-ignore]
    type: str | None = ... # type:ignore[assignment,unused-ignore]
    text: str | None = ... # type:ignore[assignment,unused-ignore]
    image_url: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union2__image_url | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str | None = ... # type:ignore[assignment,unused-ignore]
    tool_call_id: str | None = ... # type:ignore[assignment,unused-ignore]
    content: str | JsArray[Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union1__array] | Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__messages__array__content__Union2 | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Meta_Llama_4_Scout_17B_16E_Instruct_Messages_Inner_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Qwen_Qwen3_30B_A3B_Fp8_Messages_1_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class ResponsesFunctionTool__parameters__Union0(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ResponsesFunctionTool(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    parameters: ResponsesFunctionTool__parameters__Union0 | None = ... # type:ignore[assignment,unused-ignore]
    strict: bool | None = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function"] = ... # type:ignore[assignment,unused-ignore]
    description: str | None = ... # type:ignore[assignment,unused-ignore]

class EasyInputMessage(Protocol): # type:ignore[misc, unused-ignore]
    content: str | ResponseInputMessageContentList = ... # type:ignore[assignment,unused-ignore]
    role: Literal["user", "assistant", "system", "developer"] = ... # type:ignore[assignment,unused-ignore]
    type: Literal["message"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseInputItemMessage(Protocol): # type:ignore[misc, unused-ignore]
    content: ResponseInputMessageContentList = ... # type:ignore[assignment,unused-ignore]
    role: Literal["user", "system", "developer"] = ... # type:ignore[assignment,unused-ignore]
    status: Literal["in_progress", "completed", "incomplete"] | None = ... # type:ignore[assignment,unused-ignore]
    type: Literal["message"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseOutputMessage(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    content: ArrayLike_iface[ResponseOutputText | ResponseOutputRefusal] = ... # type:ignore[assignment,unused-ignore]
    role: Literal["assistant"] = ... # type:ignore[assignment,unused-ignore]
    status: Literal["in_progress", "completed", "incomplete"] = ... # type:ignore[assignment,unused-ignore]
    type: Literal["message"] = ... # type:ignore[assignment,unused-ignore]

class ResponseFunctionToolCall(Protocol): # type:ignore[misc, unused-ignore]
    arguments: str = ... # type:ignore[assignment,unused-ignore]
    call_id: str = ... # type:ignore[assignment,unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function_call"] = ... # type:ignore[assignment,unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    status: Literal["in_progress", "completed", "incomplete"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseInputItemFunctionCallOutput(Protocol): # type:ignore[misc, unused-ignore]
    call_id: str = ... # type:ignore[assignment,unused-ignore]
    output: str | ResponseFunctionCallOutputItemList = ... # type:ignore[assignment,unused-ignore]
    type: Literal["function_call_output"] = ... # type:ignore[assignment,unused-ignore]
    id: str | None = ... # type:ignore[assignment,unused-ignore]
    status: Literal["in_progress", "completed", "incomplete"] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseReasoningItem(Protocol): # type:ignore[misc, unused-ignore]
    id: str = ... # type:ignore[assignment,unused-ignore]
    summary: ArrayLike_iface[ResponseReasoningSummaryItem] = ... # type:ignore[assignment,unused-ignore]
    type: Literal["reasoning"] = ... # type:ignore[assignment,unused-ignore]
    content: ArrayLike_iface[ResponseReasoningContentItem] | None = ... # type:ignore[assignment,unused-ignore]
    encrypted_content: str | None = ... # type:ignore[assignment,unused-ignore]
    status: Literal["in_progress", "completed", "incomplete"] | None = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__messages__array(Protocol): # type:ignore[misc, unused-ignore]
    role: str = ... # type:ignore[assignment,unused-ignore]
    content: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__functions__array(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    code: str = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union0__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function__parameters__properties(Protocol): # type:ignore[misc, unused-ignore]
    pass

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function__parameters(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    required: JsArray[str] | None = ... # type:ignore[assignment,unused-ignore]
    properties: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function__parameters__properties = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    description: str = ... # type:ignore[assignment,unused-ignore]
    parameters: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function__parameters = ... # type:ignore[assignment,unused-ignore]

class Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1(Protocol): # type:ignore[misc, unused-ignore]
    type: str = ... # type:ignore[assignment,unused-ignore]
    function: Ai_Cf_Aisingapore_Gemma_Sea_Lion_V4_27B_It_Messages_1_iface__tools__array__Union1__function = ... # type:ignore[assignment,unused-ignore]

class GatewayRetries(Protocol): # type:ignore[misc, unused-ignore]
    maxAttempts: Literal[1, 2, 3, 4, 5] | None = ... # type:ignore[assignment,unused-ignore]
    retryDelayMs: int | float | None = ... # type:ignore[assignment,unused-ignore]
    backoff: Literal['constant', 'linear', 'exponential'] | None = ... # type:ignore[assignment,unused-ignore]

class EmbeddedImageConversionOptions__Intersection0(Protocol): # type:ignore[misc, unused-ignore]
    descriptionLanguage: Literal['en', 'es', 'fr', 'it', 'pt', 'de'] | None = ... # type:ignore[assignment,unused-ignore]

class EmbeddedImageConversionOptions__Intersection1(Protocol): # type:ignore[misc, unused-ignore]
    convert: bool | None = ... # type:ignore[assignment,unused-ignore]
    maxConvertedImages: int | float | None = ... # type:ignore[assignment,unused-ignore]

class EmbeddedImageConversionOptions(EmbeddedImageConversionOptions__Intersection1, EmbeddedImageConversionOptions__Intersection0, Protocol): # type:ignore[misc, unused-ignore]
    pass

class ImageConversionOptions(Protocol): # type:ignore[misc, unused-ignore]
    descriptionLanguage: Literal['en', 'es', 'fr', 'it', 'pt', 'de'] | None = ... # type:ignore[assignment,unused-ignore]

class D1Meta_iface__timings(Protocol): # type:ignore[misc, unused-ignore]
    sql_duration_ms: int | float = ... # type:ignore[assignment,unused-ignore]

class ResponseFormatText(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["text"] = ... # type:ignore[assignment,unused-ignore]

class ResponseFormatTextJSONSchemaConfig__schema(Protocol): # type:ignore[misc, unused-ignore]
    pass

class ResponseFormatTextJSONSchemaConfig(Protocol): # type:ignore[misc, unused-ignore]
    name: str = ... # type:ignore[assignment,unused-ignore]
    schema: ResponseFormatTextJSONSchemaConfig__schema = ... # type:ignore[assignment,unused-ignore]
    type: Literal["json_schema"] = ... # type:ignore[assignment,unused-ignore]
    description: str | None = ... # type:ignore[assignment,unused-ignore]
    strict: bool | None = ... # type:ignore[assignment,unused-ignore]

class ResponseFormatJSONObject(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["json_object"] = ... # type:ignore[assignment,unused-ignore]

class ResponseOutputText(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["output_text"] = ... # type:ignore[assignment,unused-ignore]
    logprobs: ArrayLike_iface[Logprob] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseOutputRefusal(Protocol): # type:ignore[misc, unused-ignore]
    refusal: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["refusal"] = ... # type:ignore[assignment,unused-ignore]

class ResponseReasoningSummaryItem(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["summary_text"] = ... # type:ignore[assignment,unused-ignore]

class ResponseReasoningContentItem(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["reasoning_text"] = ... # type:ignore[assignment,unused-ignore]

class Logprob(Protocol): # type:ignore[misc, unused-ignore]
    token: str = ... # type:ignore[assignment,unused-ignore]
    logprob: int | float = ... # type:ignore[assignment,unused-ignore]
    top_logprobs: ArrayLike_iface[TopLogprob] | None = ... # type:ignore[assignment,unused-ignore]

class ResponseInputText(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["input_text"] = ... # type:ignore[assignment,unused-ignore]

class ResponseInputImage(Protocol): # type:ignore[misc, unused-ignore]
    detail: Literal["low", "high", "auto"] = ... # type:ignore[assignment,unused-ignore]
    type: Literal["input_image"] = ... # type:ignore[assignment,unused-ignore]
    image_url: str | None = ... # type:ignore[assignment,unused-ignore]

class TopLogprob(Protocol): # type:ignore[misc, unused-ignore]
    token: str | None = ... # type:ignore[assignment,unused-ignore]
    logprob: int | float | None = ... # type:ignore[assignment,unused-ignore]

class ResponseInputTextContent(Protocol): # type:ignore[misc, unused-ignore]
    text: str = ... # type:ignore[assignment,unused-ignore]
    type: Literal["input_text"] = ... # type:ignore[assignment,unused-ignore]

class ResponseInputImageContent(Protocol): # type:ignore[misc, unused-ignore]
    type: Literal["input_image"] = ... # type:ignore[assignment,unused-ignore]
    detail: Literal["low", "high", "auto"] | None = ... # type:ignore[assignment,unused-ignore]
    image_url: str | None = ... # type:ignore[assignment,unused-ignore]

