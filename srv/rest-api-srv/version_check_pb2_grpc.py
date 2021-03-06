# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import version_check_pb2 as version__check__pb2


class VersionCheckSrvStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.VersionCheck = channel.unary_unary(
                '/VersionCheckSrv/VersionCheck',
                request_serializer=version__check__pb2.VersionCheckRequest.SerializeToString,
                response_deserializer=version__check__pb2.VersionCheckResponse.FromString,
                )


class VersionCheckSrvServicer(object):
    """Missing associated documentation comment in .proto file."""

    def VersionCheck(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VersionCheckSrvServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'VersionCheck': grpc.unary_unary_rpc_method_handler(
                    servicer.VersionCheck,
                    request_deserializer=version__check__pb2.VersionCheckRequest.FromString,
                    response_serializer=version__check__pb2.VersionCheckResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'VersionCheckSrv', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VersionCheckSrv(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def VersionCheck(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/VersionCheckSrv/VersionCheck',
            version__check__pb2.VersionCheckRequest.SerializeToString,
            version__check__pb2.VersionCheckResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
